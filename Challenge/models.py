from pydantic import BaseModel
from typing import Optional

# Category Models
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

class Category(CategoryBase):
    id: int

# Recipe Models
class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: str
    instructions: str
    cuisine: str
    difficulty: str
    category_id: Optional[int] = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

class RecipeResponse(Recipe):
    pass

