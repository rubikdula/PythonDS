# Recipe Router Application

A full-stack web application for managing recipes and categories using FastAPI, Streamlit, SQLite3, and Pydantic.

## Project Structure

```
Challenge/
├── models.py           # Pydantic models for recipes and categories
├── database.py         # SQLite3 database operations
├── main.py            # FastAPI backend server
├── streamlit_app.py   # Streamlit frontend interface
├── requirements.txt   # Python dependencies
└── recipes.db         # SQLite database (auto-created)
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd C:\Users\User\Documents\GitHub\PythonDS\Challenge
pip install -r requirements.txt
```

### 2. Run the FastAPI Backend

In one terminal/PowerShell window:

```bash
cd C:\Users\User\Documents\GitHub\PythonDS\Challenge
python -m uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`
API Documentation: `http://127.0.0.1:8000/docs`

### 3. Run the Streamlit Frontend

In a new terminal/PowerShell window:

```bash
cd C:\Users\User\Documents\GitHub\PythonDS\Challenge
streamlit run streamlit_app.py
```

The Streamlit app will open in your browser at: `http://localhost:8501`

## Features

### 📚 Recipes Management
- **View All Recipes**: Browse all recipes in the database
- **Create Recipe**: Add new recipes with name, description, ingredients, instructions, cuisine, and difficulty level
- **Update Recipe**: Modify existing recipes
- **Delete Recipe**: Remove recipes from the database
- **Search Recipes**: Filter recipes by cuisine and difficulty level

### 🏷️ Categories Management
- **View All Categories**: See all recipe categories
- **Create Category**: Add new categories
- **Update Category**: Modify category names
- **Delete Category**: Remove categories from the database

## API Endpoints

### Categories
- `GET /categories/` - Retrieve all categories
- `POST /categories/` - Create a new category
- `PUT /categories/{category_id}` - Update a category
- `DELETE /categories/{category_id}` - Delete a category

### Recipes
- `GET /recipes/` - Retrieve all recipes (with optional filters: `cuisine`, `difficulty`)
- `GET /recipes/{recipe_id}` - Get a specific recipe
- `POST /recipes/` - Create a new recipe
- `PUT /recipes/{recipe_id}` - Update a recipe
- `DELETE /recipes/{recipe_id}` - Delete a recipe

## Models

### Category
```python
{
  "id": int,
  "name": str
}
```

### Recipe
```python
{
  "id": int,
  "name": str,
  "description": str (optional),
  "ingredients": str,
  "instructions": str,
  "cuisine": str,
  "difficulty": str,
  "category_id": int (optional)
}
```

## Example Usage

### Creating a Category via API
```bash
curl -X POST "http://127.0.0.1:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Italian"}'
```

### Creating a Recipe via API
```bash
curl -X POST "http://127.0.0.1:8000/recipes/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pasta Carbonara",
    "description": "Classic Italian pasta dish",
    "ingredients": "Pasta, eggs, bacon, cheese",
    "instructions": "Cook pasta, mix with eggs and bacon",
    "cuisine": "Italian",
    "difficulty": "Medium",
    "category_id": 1
  }'
```

### Getting all recipes with filters
```bash
curl "http://127.0.0.1:8000/recipes/?cuisine=Italian&difficulty=Medium"
```

## Database Schema

The application automatically creates an SQLite database with two tables:

### categories table
```sql
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
)
```

### recipes table
```sql
CREATE TABLE recipes (
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
```

## Technology Stack

- **Backend**: FastAPI - Modern web framework for building APIs
- **Database**: SQLite3 - Lightweight embedded database
- **Data Validation**: Pydantic - Data validation using Python type annotations
- **Frontend**: Streamlit - Rapid web app development framework
- **Server**: Uvicorn - ASGI web server
- **HTTP Client**: Requests - HTTP library for Python

## Notes

- The database file `recipes.db` is created automatically in the Challenge directory
- Both the backend and frontend must be running for the Streamlit app to work
- The Streamlit frontend communicates with the FastAPI backend via HTTP requests
- All data is persisted in the SQLite database

