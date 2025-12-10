from fastapi import FastAPI, HTTPException
from typing import List, Optional
import database
from models import Recipe, RecipeCreate, Category, CategoryCreate, RecipeResponse

app = FastAPI(title="Recipe Router API", version="1.0.0")

# Category Routes
@app.get("/categories/", response_model=List[Category])
def get_categories():
    """Retrieve all categories from the database."""
    return database.get_categories()

@app.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate):
    """Create a new category in the database."""
    return database.create_category(category)

@app.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate):
    """Update the name of an existing category by its ID."""
    updated = database.update_category(category_id, category)
    if updated is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    """Delete a category from the database by ID."""
    success = database.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# Recipe Routes
@app.get("/recipes/", response_model=List[Recipe])
def get_recipes(cuisine: Optional[str] = None, difficulty: Optional[str] = None):
    """Retrieve recipes from the database with optional filters for cuisine and difficulty."""
    return database.get_recipes(cuisine=cuisine, difficulty=difficulty)

@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe in the database."""
    if recipe.category_id and not database.category_exists(recipe.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return database.create_recipe(recipe)

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe_by_id(recipe_id: int):
    """Retrieve a specific recipe by its ID."""
    recipes = database.get_recipes()
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    """Update an existing recipe in the database."""
    if recipe.category_id and not database.category_exists(recipe.category_id):
        raise HTTPException(status_code=404, detail="Category not found")

    updated = database.update_recipe(recipe_id, recipe)
    if updated is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    """Delete a recipe from the database by ID."""
    success = database.delete_recipe(recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}

@app.get("/")
def root():
    """Welcome endpoint."""
    return {"message": "Welcome to the Recipe Router API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

