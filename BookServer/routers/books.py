import sqlite3
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from BookServer.models.book import Book, BookCreate
from BookServer.database import get_db_connection
from BookServer.auth.security import get_api_key
router = APIRouter()

@router.get("/", response_model=List[Book])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, link, average_rating, published, genres FROM books")
    books = cursor.fetchall()
    conn.close()
    return [
        {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "link": book[3],
            "average_rating": book[4],
            "published": book[5],
            "genres": book[6].split(', ') if book[6] else []
        }
        for book in books
    ]

@router.post("/", response_model=Book)
def create_book(book: BookCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        genres = ", ".join(book.genres) if book.genres else None
        cursor.execute(
            "INSERT INTO books (title, author, link, average_rating, published, genres) VALUES (?, ?, ?, ?, ?, ?)",
            (book.title, book.author, book.link, book.average_rating, book.published, ', '.join(book.genres))
        )
        conn.commit()
        book_id = cursor.lastrowid
        return Book(
            id=book_id,
            title=book.title,
            author=book.author,
            link=book.link,
            average_rating=book.average_rating,
            published=book.published,
            genres=book.genres
        )
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with title '{book.title}' already exists.")
    finally:
        conn.close()

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    genres = ", ".join(book.genres)
    cursor.execute(
        "UPDATE books SET title = ?, author = ?, link = ?, average_rating = ?, published = ?, genres = ? WHERE id = ?",
        (book.title, book.author, book.link, book.average_rating, book.published, genres, book_id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id '{book_id}' not found.")
    conn.commit()
    conn.close()
    return Book(id=book_id,*book.dict())


@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: int, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id =?", (book_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id '{book_id}' not found.")
    conn.commit()
    conn.close()
    return {"detail": f"Book with id '{book_id}' deleted successfully."}
