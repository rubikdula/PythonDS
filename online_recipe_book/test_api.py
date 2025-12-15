import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_categories():
    print("Testing Categories...")
    # Create
    cat_data = {"name": "Test Category"}
    r = requests.post(f"{BASE_URL}/categories/", json=cat_data)
    if r.status_code != 200:
        print(f"Create Category Failed: {r.text}")
        return None
    cat = r.json()
    print(f"Created Category: {cat}")
    cat_id = cat['id']

    # Get All
    r = requests.get(f"{BASE_URL}/categories/")
    cats = r.json()
    print(f"All Categories: {len(cats)}")

    # Update
    cat_data['name'] = "Updated Category"
    r = requests.put(f"{BASE_URL}/categories/{cat_id}", json=cat_data)
    if r.status_code != 200:
        print(f"Update Category Failed: {r.text}")
    else:
        print(f"Updated Category: {r.json()}")

    # Delete
    r = requests.delete(f"{BASE_URL}/categories/{cat_id}")
    if r.status_code != 200:
        print(f"Delete Category Failed: {r.text}")
    else:
        print("Deleted Category")

    return cat_id # Return ID even if deleted to show we had one, or maybe create another for recipe test

def test_recipes():
    print("\nTesting Recipes...")
    # Create a category first
    r = requests.post(f"{BASE_URL}/categories/", json={"name": "Italian"})
    cat_id = r.json()['id']

    # Create Recipe
    recipe_data = {
        "name": "Pasta",
        "description": "Delicious pasta",
        "ingredients": "Noodles, Sauce",
        "instructions": "Boil water, cook noodles",
        "cuisine": "Italian",
        "difficulty": "Easy",
        "category_id": cat_id
    }
    r = requests.post(f"{BASE_URL}/recipes/", json=recipe_data)
    if r.status_code != 200:
        print(f"Create Recipe Failed: {r.text}")
        return
    recipe = r.json()
    print(f"Created Recipe: {recipe}")
    recipe_id = recipe['id']

    # Get All
    r = requests.get(f"{BASE_URL}/recipes/")
    recipes = r.json()
    print(f"All Recipes: {len(recipes)}")

    # Update
    recipe_data['name'] = "Spaghetti"
    r = requests.put(f"{BASE_URL}/recipes/{recipe_id}", json=recipe_data)
    if r.status_code != 200:
        print(f"Update Recipe Failed: {r.text}")
    else:
        print(f"Updated Recipe: {r.json()}")

    # Delete
    r = requests.delete(f"{BASE_URL}/recipes/{recipe_id}")
    if r.status_code != 200:
        print(f"Delete Recipe Failed: {r.text}")
    else:
        print("Deleted Recipe")

if __name__ == "__main__":
    try:
        test_categories()
        test_recipes()
    except Exception as e:
        print(f"Error: {e}")

