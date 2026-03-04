"""
Web scraper for extracting news article content from URLs and RSS feeds.
"""

import re
import requests
import feedparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Optional


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ---------------------------------------------------------------------------
# Article scraper
# ---------------------------------------------------------------------------

def scrape_article(url: str) -> dict:
    """Scrape a news article from a URL and return structured data."""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")

    # Remove noisy tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
        tag.decompose()

    # --- Title ---
    title = _extract_title(soup)

    # --- Body content ---
    content = _extract_content(soup)

    # --- Author ---
    author = _extract_author(soup)

    domain = urlparse(url).netloc.replace("www.", "")

    return {
        "title": title or "Unknown Title",
        "content": content,
        "author": author or f"Source: {domain}",
        "url": url,
        "domain": domain,
        "word_count": len(content.split()) if content else 0,
    }


def _extract_title(soup: BeautifulSoup) -> str:
    # OpenGraph first
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text().strip()
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text().strip()
    return ""


def _extract_content(soup: BeautifulSoup) -> str:
    # Semantic selectors in priority order
    selectors = [
        "article",
        '[role="main"]',
        ".article-body",
        ".article-content",
        ".post-content",
        ".entry-content",
        ".story-body",
        ".story-content",
        ".article__body",
        "main",
    ]
    for sel in selectors:
        elem = soup.select_one(sel)
        if elem:
            paras = elem.find_all("p")
            text = " ".join(
                p.get_text().strip()
                for p in paras
                if len(p.get_text().strip()) > 25
            )
            if len(text) > 200:
                return _clean_text(text)

    # Fallback: all paragraphs
    paras = soup.find_all("p")
    text = " ".join(
        p.get_text().strip() for p in paras if len(p.get_text().strip()) > 25
    )
    return _clean_text(text)


def _extract_author(soup: BeautifulSoup) -> str:
    meta_names = [
        {"name": "author"},
        {"property": "article:author"},
        {"name": "dc.creator"},
        {"name": "DC.creator"},
    ]
    for attrs in meta_names:
        meta = soup.find("meta", attrs)
        if meta and meta.get("content"):
            return meta["content"].strip()

    for css in [".author", ".byline", '[rel="author"]', ".article-author"]:
        elem = soup.select_one(css)
        if elem:
            return elem.get_text().strip()[:80]
    return ""


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:10000]  # Cap at 10,000 chars


# ---------------------------------------------------------------------------
# Trending news via RSS
# ---------------------------------------------------------------------------

RSS_FEEDS = {
    "BBC News":     "http://feeds.bbci.co.uk/news/rss.xml",
    "Reuters":      "https://feeds.reuters.com/reuters/topNews",
    "NPR News":     "https://feeds.npr.org/1001/rss.xml",
    "Al Jazeera":   "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
}


def fetch_trending(source: str = "BBC News", max_items: int = 15) -> list:
    """
    Return a list of trending news articles from an RSS feed.
    Each item: { title, link, summary, published, source }
    """
    url = RSS_FEEDS.get(source)
    if not url:
        return []

    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:max_items]:
        items.append({
            "title":     entry.get("title", "No Title"),
            "link":      entry.get("link", ""),
            "summary":   _clean_text(entry.get("summary", "")),
            "published": entry.get("published", ""),
            "source":    source,
        })
    return items


def get_available_sources() -> list:
    return list(RSS_FEEDS.keys())
