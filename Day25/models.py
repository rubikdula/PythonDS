from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    overview: str

class Movie(MovieCreate):
    id: int