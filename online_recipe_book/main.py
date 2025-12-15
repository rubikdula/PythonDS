from fastapi import FastAPI

from online_recipe_book.routers import recipes, categories

app = FastAPI(title="Online Recipe Book API")

app.include_router(recipes.router)
app.include_router(categories.router)

@app.get("/")
def root():
    return {"message": "Online Recipe Book API is running"}

