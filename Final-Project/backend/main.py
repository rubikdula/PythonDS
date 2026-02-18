from fastapi import FastAPI, Depends, HTTPException
from typing import List
import random
import sqlite3
from pydantic import BaseModel

from . import database  # models is removed

# Initialize DB (creates table if not exists)
try:
    database.init_db()
except Exception as e:
    print(f"DB Init Error: {e}")

app = FastAPI()


# Dependency
def get_db():
    conn = database.get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


class CheckRequest(BaseModel):
    text: str
    title: str = "Untitled"
    author: str = "Anonymous"


class CheckResponse(BaseModel):
    verdict: str
    confidence: float
    flags: List[str] = []


class HistoryItem(BaseModel):
    id: int
    title: str

    content: str
    author: str
    verdict: str
    confidence_score: float

    class Config:
        orm_mode = True


@app.post("/predict", response_model=CheckResponse)
def predict_news(request: CheckRequest, db: sqlite3.Connection = Depends(get_db)):
    # ---------------------------------------------------------
    # Simple "AI" Logic for Prototype
    # ---------------------------------------------------------
    fake_keywords = ["proven", "guaranteed", "secret", "won't believe", "shocking", "miracle", "banned"]
    text_lower = request.text.lower()

    # Default baseline
    is_fake = False
    confidence = 0.70
    detected_flags = []

    # Heuristic 1: Length check
    if len(request.text) < 50:
        is_fake = True
        confidence = 0.95
        detected_flags.append("Text too short")

    # Heuristic 2: Keyword check
    found_keywords = [kw for kw in fake_keywords if kw in text_lower]
    if found_keywords:
        is_fake = True
        confidence = 0.88 + (random.random() * 0.1)
        detected_flags.extend([f"Suspicious word: '{kw}'" for kw in found_keywords])

    if not is_fake:
        # Heuristic 3: Random simulation for "complex" articles
        # In a real app, model.predict(text) would go here
        val = random.random()
        if val > 0.5:
            is_fake = True
            confidence = 0.60 + (val * 0.3)
            detected_flags.append("AI Pattern Match")
        else:
            is_fake = False
            confidence = 0.75 + (val * 0.2)
            detected_flags.append("Verified Source Pattern")

    verdict = "Fake" if is_fake else "Real"

    # Store in Database
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO news_articles (title, content, author, verdict, confidence_score) VALUES (?, ?, ?, ?, ?)",
            (request.title, request.text, request.author, verdict, confidence)
        )
        db.commit()
    except Exception as e:
        print(f"Error saving to DB: {e}")

    return {"verdict": verdict, "confidence": confidence, "flags": detected_flags}


@app.get("/stats")
def get_stats(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # Total count
    cursor.execute("SELECT COUNT(*) FROM news_articles")
    row = cursor.fetchone()
    total = row[0] if row else 0

    # Fake count
    cursor.execute("SELECT COUNT(*) FROM news_articles WHERE verdict = 'Fake'")
    row = cursor.fetchone()
    fake_count = row[0] if row else 0

    # Real count
    cursor.execute("SELECT COUNT(*) FROM news_articles WHERE verdict = 'Real'")
    row = cursor.fetchone()
    real_count = row[0] if row else 0

    # Avg confidence
    cursor.execute("SELECT AVG(confidence_score) FROM news_articles")
    row = cursor.fetchone()
    avg_conf = row[0] if row and row[0] is not None else 0

    return {
        "total_scans": total,
        "fake_count": fake_count,
        "real_count": real_count,
        "avg_confidence": avg_conf
    }


@app.get("/history", response_model=List[HistoryItem])
def get_history(db: sqlite3.Connection = Depends(get_db)):
    # Return all articles, newest first
    cursor = db.cursor()
    cursor.execute("SELECT id, title, content, author, verdict, confidence_score FROM news_articles ORDER BY id DESC")
    rows = cursor.fetchall()  # rows are sqlite3.Row objects (dict-like)

    # Convert sqlite3.Row objects to dictionaries for Pydantic
    return [dict(row) for row in rows]
