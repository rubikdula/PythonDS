from fastapi import APIRouter, HTTPException
from typing import List

from online_recipe_book.models.category import Category, CategoryCreate
from online_recipe_book import database

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[Category])
def list_categories():
    return database.get_categories()

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate):
    return database.create_category(category)

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate):
    updated = database.update_category(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}")
def delete_category(category_id: int):
    deleted = database.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted"}

