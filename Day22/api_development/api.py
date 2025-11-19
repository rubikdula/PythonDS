from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

class Person(BaseModel):
    name: str
    age: int

@app.post("/users/")
async def create_user(user: User):
    return {"message": "User created successfully", "user": user}

@app.post("/persons/")
async def create_person(person: Person):
    return {"message": f"Person {person.name} created with age {person.age} successfully"}