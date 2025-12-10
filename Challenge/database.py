import sqlite3
from typing import List, Optional
from models import Recipe, RecipeCreate, Category, CategoryCreate

DATABASE = 'recipes.db'

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Create recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    conn.commit()
    conn.close()

# Category Functions
def get_categories() -> List[Category]:
    """Retrieve all categories from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    rows = cursor.fetchall()
    conn.close()
    return [Category(id=row['id'], name=row['name']) for row in rows]

def create_category(category: CategoryCreate) -> Category:
    """Create a new category in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO categories (name) VALUES (?)', (category.name,))
    conn.commit()
    category_id = cursor.lastrowid
    conn.close()
    return Category(id=category_id, name=category.name)

def update_category(category_id: int, category: CategoryCreate) -> Optional[Category]:
    """Update an existing category by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (category.name, category_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated > 0:
        return Category(id=category_id, name=category.name)
    return None

def delete_category(category_id: int) -> bool:
    """Delete a category from the database by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0

def category_exists(category_id: int) -> bool:
    """Check if a category with the given ID exists in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM categories WHERE id = ?', (category_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Recipe Functions
def get_recipes(cuisine: Optional[str] = None, difficulty: Optional[str] = None) -> List[Recipe]:
    """Retrieve recipes from the database with optional filters for cuisine and difficulty."""
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM recipes WHERE 1=1'
    params = []

    if cuisine:
        query += ' AND cuisine = ?'
        params.append(cuisine)
    if difficulty:
        query += ' AND difficulty = ?'
        params.append(difficulty)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [Recipe(
        id=row['id'],
        name=row['name'],
        description=row['description'],
        ingredients=row['ingredients'],
        instructions=row['instructions'],
        cuisine=row['cuisine'],
        difficulty=row['difficulty'],
        category_id=row['category_id']
    ) for row in rows]

def create_recipe(recipe: RecipeCreate) -> Recipe:
    """Create a new recipe in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO recipes 
           (name, description, ingredients, instructions, cuisine, difficulty, category_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (recipe.name, recipe.description, recipe.ingredients, recipe.instructions,
         recipe.cuisine, recipe.difficulty, recipe.category_id)
    )
    conn.commit()
    recipe_id = cursor.lastrowid
    conn.close()

    return Recipe(
        id=recipe_id,
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        cuisine=recipe.cuisine,
        difficulty=recipe.difficulty,
        category_id=recipe.category_id
    )

def update_recipe(recipe_id: int, recipe: RecipeCreate) -> Optional[Recipe]:
    """Update an existing recipe in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE recipes 
           SET name = ?, description = ?, ingredients = ?, instructions = ?,
               cuisine = ?, difficulty = ?, category_id = ?
           WHERE id = ?''',
        (recipe.name, recipe.description, recipe.ingredients, recipe.instructions,
         recipe.cuisine, recipe.difficulty, recipe.category_id, recipe_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated > 0:
        return Recipe(
            id=recipe_id,
            name=recipe.name,
            description=recipe.description,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            cuisine=recipe.cuisine,
            difficulty=recipe.difficulty,
            category_id=recipe.category_id
        )
    return None

def delete_recipe(recipe_id: int) -> bool:
    """Delete a recipe from the database by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0

# Initialize database on import
init_db()

