from fastapi import FastAPI
from BookServer.routers import books, authors, api_key
from BookServer.database import create_database
from auth.security import get_api_key

app = FastAPI(
    title="BookServer API",
    description="An API for managing books and authors.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    create_database()

app.include_router(authors.router, prefix="/api/authors", tags=["Authors"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(api_key.router, prefix="/api/api_key", tags=["API Key"])