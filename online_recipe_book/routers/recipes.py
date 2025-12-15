from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from online_recipe_book.models.recipe import Recipe, RecipeCreate, RecipeResponse
from online_recipe_book import database

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/", response_model=List[RecipeResponse])
def list_recipes(cuisine: Optional[str] = Query(None), difficulty: Optional[str] = Query(None)):
    """List recipes with optional filters."""
    recipes = database.get_recipes(cuisine=cuisine, difficulty=difficulty)
    return recipes

@router.post("/", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate):
    created = database.create_recipe(recipe)
    return created

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    updated = database.update_recipe(recipe_id, recipe)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int):
    deleted = database.delete_recipe(recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"detail": "Recipe deleted"}

