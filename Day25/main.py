from fastapi import FastAPI
from typing import List
import database
import models
from models import Movie, MovieCreate

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD Movies API!"}

@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate):
    """Create a new movie."""
    movie_id = create_movie(movie)
    return models.Movie(id=movie_id, **movie.dict())

@app.get("/movies/", response_model=list[Movie])
def read_movies():
    """Read all movies."""
    return database.read_movies()

@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie_by_id(movie_id: int):
    """Read a movie by its ID."""
    movie = database.read_movie_by_id(movie_id)
    if movie is None:
        raise HTTPExeption(status_code=404, detail="Movie not found")
    return movie