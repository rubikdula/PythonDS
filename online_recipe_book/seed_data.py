import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def seed_data():
    print("Seeding data...")

    # Categories to add
    categories = [
        "Italian",
        "Mexican",
        "Indian",
        "Chinese",
        "American",
        "Dessert",
        "Breakfast",
        "Vegetarian"
    ]

    category_map = {}

    print("Adding Categories...")
    for cat_name in categories:
        try:
            # Check if exists first (optional, but good for re-running)
            # For simplicity, we just try to create. If duplicate, it might fail or create duplicate depending on backend logic.
            # The backend uses `name TEXT NOT NULL UNIQUE` so it will fail if exists.
            # We should probably handle that or just ignore errors.

            # Actually, let's just try to create and catch error if it exists, or check if we can get it.
            # Since we don't have a search by name endpoint easily accessible without fetching all, let's fetch all first.
            pass
        except Exception:
            pass

    # Fetch existing categories to avoid duplicates and get IDs
    try:
        r = requests.get(f"{BASE_URL}/categories/")
        if r.status_code == 200:
            existing_cats = {c['name']: c['id'] for c in r.json()}
        else:
            print("Failed to fetch categories. Is the server running?")
            return
    except requests.exceptions.ConnectionError:
        print("Connection refused. Please ensure the FastAPI server is running on port 8000.")
        return

    for cat_name in categories:
        if cat_name not in existing_cats:
            r = requests.post(f"{BASE_URL}/categories/", json={"name": cat_name})
            if r.status_code == 200:
                cat_id = r.json()['id']
                category_map[cat_name] = cat_id
                print(f"Created category: {cat_name}")
            else:
                print(f"Failed to create category {cat_name}: {r.text}")
        else:
            category_map[cat_name] = existing_cats[cat_name]
            print(f"Category already exists: {cat_name}")

    # Recipes to add
    recipes = [
        {
            "name": "Spaghetti Carbonara",
            "description": "Classic Italian pasta dish with eggs, cheese, pancetta, and pepper.",
            "ingredients": "Spaghetti, Eggs, Pecorino Romano, Pancetta, Black Pepper",
            "instructions": "1. Boil pasta. 2. Fry pancetta. 3. Mix eggs and cheese. 4. Combine all with pasta water.",
            "cuisine": "Italian",
            "difficulty": "Medium",
            "category_name": "Italian"
        },
        {
            "name": "Chicken Tikka Masala",
            "description": "Chunks of roasted marinated chicken in a spiced curry sauce.",
            "ingredients": "Chicken, Yogurt, Spices, Tomato Sauce, Cream",
            "instructions": "1. Marinate chicken. 2. Grill chicken. 3. Make sauce. 4. Simmer chicken in sauce.",
            "cuisine": "Indian",
            "difficulty": "Hard",
            "category_name": "Indian"
        },
        {
            "name": "Tacos al Pastor",
            "description": "Tacos made with spit-grilled pork.",
            "ingredients": "Pork, Pineapple, Corn Tortillas, Onion, Cilantro",
            "instructions": "1. Marinate pork. 2. Grill pork with pineapple. 3. Serve on tortillas.",
            "cuisine": "Mexican",
            "difficulty": "Medium",
            "category_name": "Mexican"
        },
        {
            "name": "Kung Pao Chicken",
            "description": "Spicy, stir-fried Chinese dish made with cubes of chicken, peanuts, vegetables, and chili peppers.",
            "ingredients": "Chicken, Peanuts, Chili Peppers, Vegetables, Soy Sauce",
            "instructions": "1. Stir fry chicken. 2. Add vegetables and peanuts. 3. Add sauce.",
            "cuisine": "Chinese",
            "difficulty": "Medium",
            "category_name": "Chinese"
        },
        {
            "name": "Cheeseburger",
            "description": "Juicy grilled beef patty with cheese in a bun.",
            "ingredients": "Ground Beef, Bun, Cheese, Lettuce, Tomato, Onion",
            "instructions": "1. Grill patty. 2. Melt cheese on top. 3. Assemble burger.",
            "cuisine": "American",
            "difficulty": "Easy",
            "category_name": "American"
        },
        {
            "name": "Chocolate Cake",
            "description": "Rich and moist chocolate cake.",
            "ingredients": "Flour, Sugar, Cocoa Powder, Eggs, Milk, Butter",
            "instructions": "1. Mix dry ingredients. 2. Mix wet ingredients. 3. Combine and bake.",
            "cuisine": "Dessert",
            "difficulty": "Medium",
            "category_name": "Dessert"
        },
        {
            "name": "Pancakes",
            "description": "Fluffy breakfast cakes.",
            "ingredients": "Flour, Milk, Eggs, Baking Powder, Sugar",
            "instructions": "1. Mix batter. 2. Cook on griddle. 3. Serve with syrup.",
            "cuisine": "Breakfast",
            "difficulty": "Easy",
            "category_name": "Breakfast"
        },
         {
            "name": "Vegetable Stir Fry",
            "description": "Healthy mix of vegetables stir-fried in a savory sauce.",
            "ingredients": "Broccoli, Carrots, Bell Peppers, Soy Sauce, Ginger, Garlic",
            "instructions": "1. Chop veggies. 2. Stir fry with aromatics. 3. Add sauce.",
            "cuisine": "Vegetarian",
            "difficulty": "Easy",
            "category_name": "Vegetarian"
        }
    ]

    print("\nAdding Recipes...")
    for recipe in recipes:
        cat_name = recipe.pop("category_name")
        cat_id = category_map.get(cat_name)

        if cat_id:
            recipe["category_id"] = cat_id
            # Check if recipe exists (simple check by name? API doesn't support search by name exactly, but we can list all)
            # For now, just try to create.
            r = requests.post(f"{BASE_URL}/recipes/", json=recipe)
            if r.status_code == 200:
                print(f"Created recipe: {recipe['name']}")
            else:
                print(f"Failed to create recipe {recipe['name']}: {r.text}")
        else:
            print(f"Skipping {recipe['name']}: Category {cat_name} not found.")

if __name__ == "__main__":
    seed_data()

