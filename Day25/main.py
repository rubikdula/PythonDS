from fastapi import FastAPI, HTTPException
from typing import List
import database
import models
import uvicorn
from models import Movie, MovieCreate

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD Movies API!"}

@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate):
    """Create a new movie."""
    movie_id = database.create_movie(movie)
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
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/movies/{movie_id}", response_model=models.Movie)
def update_movie(movie_id: int, movie: models.MovieCreate):
    """Update a movie by its ID."""
    updated_movie = database.update_movie(movie_id, movie)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

@app.delete("/movies/{movie_id}", response_model=dict)
def delete_movie(movie_id: int):
    """Delete a movie by its ID."""
    success = database.delete_movie(movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}