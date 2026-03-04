import sqlite3
import os

DB_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

DB_PATH = os.path.join(DB_FOLDER, 'news.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            author TEXT,
            source_url TEXT DEFAULT '',
            verdict TEXT,
            confidence_score REAL,
            sentiment TEXT DEFAULT 'Neutral',
            subjectivity TEXT DEFAULT 'Objective',
            word_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Migrate existing table: add new columns if they don't exist
    existing = [row[1] for row in c.execute("PRAGMA table_info(news_articles)").fetchall()]
    # When altering an existing table, SQLite doesn't allow non-constant
    # expressions like CURRENT_TIMESTAMP as a default. For migrations we
    # therefore add simple columns without complex defaults; the CREATE
    # TABLE statement above already handles the ideal schema for new DBs.
    for col, definition in [
        ("source_url",   "TEXT DEFAULT ''"),
        ("sentiment",    "TEXT DEFAULT 'Neutral'"),
        ("subjectivity", "TEXT DEFAULT 'Objective'"),
        ("word_count",   "INTEGER DEFAULT 0"),
        ("created_at",   "DATETIME"),
    ]:
        if col not in existing:
            c.execute(f"ALTER TABLE news_articles ADD COLUMN {col} {definition}")

    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            user_feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

