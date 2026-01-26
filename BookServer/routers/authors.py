import sqlite3
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models.author import Author
from database import get_db_connection
from auth.security import get_api_key
router = APIRouter()

@router.get("/", response_model=List[Author])
def get_authors(api_key: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM authors")
    authors = cursor.fetchall()
    conn.close()
    return [{"id": author[0], "name": author[1]} for author in authors]