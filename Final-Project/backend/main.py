from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import random
import sqlite3
import re
from collections import Counter
from pydantic import BaseModel
from textblob import TextBlob

from . import database
from .scraper import scrape_article, fetch_trending, get_available_sources

# Initialize DB
try:
    database.init_db()
except Exception as e:
    print(f"DB Init Error: {e}")

app = FastAPI(title="TruthScanner AI API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

def get_db():
    conn = database.get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class CheckRequest(BaseModel):
    text: str
    title: str = "Untitled"
    author: str = "Anonymous"
    source_url: str = ""


class CheckResponse(BaseModel):
    article_id: int
    verdict: str
    confidence: float
    flags: List[str] = []
    sentiment: str = "Neutral"
    subjectivity: str = "Objective"
    top_words: dict = {}
    credibility_score: float = 0.5


class ScrapeRequest(BaseModel):
    url: str


class FeedbackRequest(BaseModel):
    article_id: int
    user_feedback: str  # "correct" or "incorrect"


class HistoryItem(BaseModel):
    id: int
    title: str
    content: str
    author: str
    source_url: str = ""
    verdict: str
    confidence_score: float
    sentiment: str = "Neutral"
    subjectivity: str = "Objective"
    word_count: int = 0
    created_at: str = ""

    class Config:
        orm_mode = True


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------

FAKE_KEYWORDS = [
    "won't believe", "shocking", "miracle", "banned", "conspiracy",
    "cover-up", "mainstream media", "wake up", "sheep", "truth about",
    "exposed", "scandal", "clickbait", "breaking:", "urgent:", "alert:",
    "secret", "proven fake", "hoax", "they don't want you to know",
    "fake news", "scam", "propaganda", "brainwashed", "sheeple",
    "the real truth", "doctors hate", "one weird trick",
]

CREDIBILITY_MARKERS = [
    "according to", "study shows", "research indicates", "experts say",
    "reported by", "official statement", "confirmed by", "data shows",
    "per the report", "sources say", "cited", "published", "peer-reviewed",
    "university", "institute", "government", "spokesperson",
]

STOP_WORDS = {
    "the","a","an","is","it","in","to","of","and","or","but","for","on",
    "at","by","with","this","that","was","are","be","as","from","its","into",
    "we","i","you","he","she","they","have","has","had","not","which","will",
    "can","more","also","their","been","were","after","about","than","all",
    "would","could","said","just","do","so","if","up","out","one","new","when",
}


def get_top_words(text: str, n: int = 10) -> dict:
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    filtered = [w for w in words if w not in STOP_WORDS]
    return dict(Counter(filtered).most_common(n))


def analyze_text(text: str):
    """Return (fake_score, flags, sentiment_label, subjectivity_label, credibility_score)."""
    try:
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity
    except Exception:
        sentiment_score = 0.0
        subjectivity_score = 0.0

    sentiment_label = "Neutral"
    if sentiment_score > 0.15:
        sentiment_label = "Positive"
    elif sentiment_score < -0.15:
        sentiment_label = "Negative"

    subjectivity_label = "Objective"
    if subjectivity_score > 0.5:
        subjectivity_label = "Subjective"

    text_lower = text.lower()
    flags = []
    fake_score = 0.0

    # Rule 1: Very short text
    if len(text) < 60:
        fake_score += 0.35
        flags.append("Text is extremely short — insufficient for analysis")

    # Rule 2: Sensationalist keywords
    found_kw = [kw for kw in FAKE_KEYWORDS if kw in text_lower]
    if found_kw:
        fake_score += min(0.5, 0.12 * len(found_kw))
        for kw in found_kw[:4]:
            flags.append(f"Sensationalist phrase detected: \"{kw}\"")
        if len(found_kw) > 4:
            flags.append(f"… and {len(found_kw) - 4} more suspicious phrases")

    # Rule 3: ALL CAPS words
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 3]
    if len(caps_words) >= 3:
        fake_score += 0.15
        flags.append(f"Excessive CAPS usage ({len(caps_words)} words)")

    # Rule 4: High subjectivity
    if subjectivity_score > 0.75:
        fake_score += 0.20
        flags.append("Highly subjective language detected")
    elif subjectivity_score > 0.5:
        fake_score += 0.08
        flags.append("Moderately subjective language")

    # Rule 5: Extreme sentiment
    if abs(sentiment_score) > 0.6:
        fake_score += 0.15
        flags.append(f"Extreme emotional sentiment ({sentiment_score:+.2f})")

    # Rule 6: Excessive exclamation marks
    exclamation_count = text.count("!")
    if exclamation_count >= 3:
        fake_score += 0.12
        flags.append(f"Excessive exclamation marks ({exclamation_count})")

    # Rule 7: Credibility markers reduce fake score
    found_cred = [m for m in CREDIBILITY_MARKERS if m in text_lower]
    credibility_bonus = min(0.3, 0.05 * len(found_cred))
    fake_score = max(0.0, fake_score - credibility_bonus)
    if found_cred:
        flags.append(f"✅ Credibility markers found: {len(found_cred)} (e.g. \"{found_cred[0]}\")")

    # Rule 8: Word count
    wc = len(text.split())
    if wc < 30:
        fake_score += 0.2
        flags.append(f"Very low word count ({wc} words)")
    elif wc > 300:
        fake_score = max(0.0, fake_score - 0.05)

    credibility_score = max(0.0, min(1.0, 1.0 - fake_score))
    return fake_score, flags, sentiment_label, subjectivity_label, credibility_score


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/predict", response_model=CheckResponse)
def predict_news(request: CheckRequest, db: sqlite3.Connection = Depends(get_db)):
    fake_score, flags, sentiment_label, subjectivity_label, credibility_score = analyze_text(request.text)
    top_words = get_top_words(request.text)

    if fake_score < 0.25:
        is_fake = False
        confidence = 0.72 + (random.random() * 0.18)
        if not [f for f in flags if not f.startswith("✅")]:
            flags.append("✅ Writing style appears credible")
    elif fake_score < 0.5:
        is_fake = bool(random.random() > 0.35)
        confidence = 0.50 + (fake_score * 0.4)
    else:
        is_fake = True
        confidence = min(0.97, 0.55 + fake_score * 0.45)

    verdict = "Fake" if is_fake else "Real"
    word_count = len(request.text.split())

    article_id = 0
    try:
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO news_articles
               (title, content, author, source_url, verdict, confidence_score,
                sentiment, subjectivity, word_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.title, request.text, request.author, request.source_url,
                verdict, confidence, sentiment_label, subjectivity_label, word_count,
            ),
        )
        article_id = cursor.lastrowid
        db.commit()
    except Exception as e:
        print(f"DB Error: {e}")

    return {
        "article_id": article_id,
        "verdict": verdict,
        "confidence": confidence,
        "flags": flags,
        "sentiment": sentiment_label,
        "subjectivity": subjectivity_label,
        "top_words": top_words,
        "credibility_score": credibility_score,
    }


@app.post("/scrape")
def scrape_url(request: ScrapeRequest):
    """Scrape an article from a URL and return its content."""
    try:
        data = scrape_article(str(request.url))
        if not data["content"]:
            raise HTTPException(status_code=422, detail="Could not extract article content from this URL.")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping failed: {str(e)}")


@app.get("/trending")
def get_trending(source: str = "BBC News", max_items: int = 15):
    """Return trending news headlines from an RSS feed."""
    try:
        items = fetch_trending(source=source, max_items=max_items)
        return {"source": source, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/trending/sources")
def get_sources():
    return {"sources": get_available_sources()}


@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO feedback (article_id, user_feedback) VALUES (?, ?)",
            (feedback.article_id, feedback.user_feedback),
        )
        db.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/feedback/all")
def get_all_feedback(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        """SELECT f.id, f.article_id, n.title, f.user_feedback, f.timestamp
           FROM feedback f
           LEFT JOIN news_articles n ON f.article_id = n.id
           ORDER BY f.timestamp DESC
           LIMIT 100"""
    )
    rows = cursor.fetchall()
    return [dict(r) for r in rows]


@app.get("/stats")
def get_stats(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM news_articles")
    total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM news_articles WHERE verdict = 'Fake'")
    fake_count = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM news_articles WHERE verdict = 'Real'")
    real_count = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(confidence_score) FROM news_articles")
    avg_conf = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM feedback")
    feedback_count = cursor.fetchone()[0] or 0

    return {
        "total_scans": total,
        "fake_count": fake_count,
        "real_count": real_count,
        "avg_confidence": avg_conf,
        "feedback_count": feedback_count,
    }


@app.get("/history", response_model=List[HistoryItem])
def get_history(limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        """SELECT id, title, content, author,
                  COALESCE(source_url, '') as source_url,
                  verdict, confidence_score,
                  COALESCE(sentiment, 'Neutral') as sentiment,
                  COALESCE(subjectivity, 'Objective') as subjectivity,
                  COALESCE(word_count, 0) as word_count,
                  COALESCE(created_at, '') as created_at
           FROM news_articles
           ORDER BY id DESC
           LIMIT ?""",
        (limit,),
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
