import streamlit as st
import requests
import json

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Recipe Router", layout="wide")
st.title("🍳 Recipe Router")
st.markdown("Manage your recipes and categories with ease!")

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Select a page:",
        ["Home", "Recipes", "Categories"]
    )

# Home Page
if page == "Home":
    st.header("Welcome to Recipe Router")
    st.markdown("""
    This application allows you to:
    - **Manage Recipes**: Create, read, update, and delete recipes
    - **Organize Categories**: Create and manage recipe categories
    - **Filter Recipes**: Search recipes by cuisine and difficulty level

    Use the navigation menu on the left to get started!
    """)

# Recipes Page
elif page == "Recipes":
    st.header("📚 Recipes")

    # Tabs for different operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["View All", "Create", "Update", "Delete", "Search"])

    # View All Recipes
    with tab1:
        st.subheader("All Recipes")
        try:
            response = requests.get(f"{API_URL}/recipes/")
            recipes = response.json()

            if recipes:
                for recipe in recipes:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(recipe['name'])
                            if recipe['description']:
                                st.write(f"**Description:** {recipe['description']}")
                            st.write(f"**Cuisine:** {recipe['cuisine']}")
                            st.write(f"**Difficulty:** {recipe['difficulty']}")
                            st.write(f"**Ingredients:** {recipe['ingredients']}")
                            st.write(f"**Instructions:** {recipe['instructions']}")
                        with col2:
                            st.caption(f"ID: {recipe['id']}")
            else:
                st.info("No recipes found. Create one to get started!")
        except Exception as e:
            st.error(f"Error fetching recipes: {str(e)}")

    # Create Recipe
    with tab2:
        st.subheader("Create a New Recipe")
        with st.form("create_recipe_form"):
            name = st.text_input("Recipe Name *")
            description = st.text_area("Description (optional)")
            ingredients = st.text_area("Ingredients *")
            instructions = st.text_area("Instructions *")

            col1, col2, col3 = st.columns(3)
            with col1:
                cuisine = st.text_input("Cuisine *")
            with col2:
                difficulty = st.selectbox("Difficulty *", ["Easy", "Medium", "Hard"])
            with col3:
                category_id = st.number_input("Category ID (optional)", value=0, step=1)

            submitted = st.form_submit_button("Create Recipe")

            if submitted:
                if name and ingredients and instructions and cuisine:
                    try:
                        recipe_data = {
                            "name": name,
                            "description": description,
                            "ingredients": ingredients,
                            "instructions": instructions,
                            "cuisine": cuisine,
                            "difficulty": difficulty,
                            "category_id": category_id if category_id > 0 else None
                        }
                        response = requests.post(f"{API_URL}/recipes/", json=recipe_data)
                        if response.status_code == 200:
                            st.success("Recipe created successfully!")
                            st.json(response.json())
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error creating recipe: {str(e)}")
                else:
                    st.error("Please fill in all required fields (*)")

    # Update Recipe
    with tab3:
        st.subheader("Update a Recipe")
        try:
            response = requests.get(f"{API_URL}/recipes/")
            recipes = response.json()
            recipe_options = {f"{r['id']} - {r['name']}": r['id'] for r in recipes}

            if recipe_options:
                selected_recipe = st.selectbox("Select Recipe to Update", recipe_options.keys())
                recipe_id = recipe_options[selected_recipe]

                # Get current recipe details
                current_recipe = next(r for r in recipes if r['id'] == recipe_id)

                with st.form("update_recipe_form"):
                    name = st.text_input("Recipe Name", value=current_recipe['name'])
                    description = st.text_area("Description", value=current_recipe['description'] or "")
                    ingredients = st.text_area("Ingredients", value=current_recipe['ingredients'])
                    instructions = st.text_area("Instructions", value=current_recipe['instructions'])

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        cuisine = st.text_input("Cuisine", value=current_recipe['cuisine'])
                    with col2:
                        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"],
                                                  index=["Easy", "Medium", "Hard"].index(current_recipe['difficulty']))
                    with col3:
                        category_id = st.number_input("Category ID", value=current_recipe['category_id'] or 0, step=1)

                    submitted = st.form_submit_button("Update Recipe")

                    if submitted:
                        try:
                            recipe_data = {
                                "name": name,
                                "description": description,
                                "ingredients": ingredients,
                                "instructions": instructions,
                                "cuisine": cuisine,
                                "difficulty": difficulty,
                                "category_id": category_id if category_id > 0 else None
                            }
                            response = requests.put(f"{API_URL}/recipes/{recipe_id}", json=recipe_data)
                            if response.status_code == 200:
                                st.success("Recipe updated successfully!")
                                st.json(response.json())
                            else:
                                st.error(f"Error: {response.text}")
                        except Exception as e:
                            st.error(f"Error updating recipe: {str(e)}")
            else:
                st.info("No recipes available to update")
        except Exception as e:
            st.error(f"Error loading recipes: {str(e)}")

    # Delete Recipe
    with tab4:
        st.subheader("Delete a Recipe")
        try:
            response = requests.get(f"{API_URL}/recipes/")
            recipes = response.json()
            recipe_options = {f"{r['id']} - {r['name']}": r['id'] for r in recipes}

            if recipe_options:
                selected_recipe = st.selectbox("Select Recipe to Delete", recipe_options.keys())
                recipe_id = recipe_options[selected_recipe]

                if st.button("Delete Recipe", type="secondary"):
                    try:
                        response = requests.delete(f"{API_URL}/recipes/{recipe_id}")
                        if response.status_code == 200:
                            st.success("Recipe deleted successfully!")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error deleting recipe: {str(e)}")
            else:
                st.info("No recipes available to delete")
        except Exception as e:
            st.error(f"Error loading recipes: {str(e)}")

    # Search Recipes
    with tab5:
        st.subheader("Search Recipes")
        col1, col2 = st.columns(2)

        with col1:
            cuisine_filter = st.text_input("Filter by Cuisine (optional)")
        with col2:
            difficulty_filter = st.selectbox("Filter by Difficulty (optional)",
                                             ["", "Easy", "Medium", "Hard"])

        if st.button("Search"):
            try:
                params = {}
                if cuisine_filter:
                    params['cuisine'] = cuisine_filter
                if difficulty_filter:
                    params['difficulty'] = difficulty_filter

                response = requests.get(f"{API_URL}/recipes/", params=params)
                recipes = response.json()

                if recipes:
                    st.success(f"Found {len(recipes)} recipe(s)")
                    for recipe in recipes:
                        with st.container(border=True):
                            st.subheader(recipe['name'])
                            if recipe['description']:
                                st.write(f"**Description:** {recipe['description']}")
                            st.write(f"**Cuisine:** {recipe['cuisine']}")
                            st.write(f"**Difficulty:** {recipe['difficulty']}")
                            st.write(f"**Ingredients:** {recipe['ingredients']}")
                            st.write(f"**Instructions:** {recipe['instructions']}")
                else:
                    st.info("No recipes found matching your search criteria")
            except Exception as e:
                st.error(f"Error searching recipes: {str(e)}")

# Categories Page
elif page == "Categories":
    st.header("🏷️ Categories")

    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])

    # View All Categories
    with tab1:
        st.subheader("All Categories")
        try:
            response = requests.get(f"{API_URL}/categories/")
            categories = response.json()

            if categories:
                cols = st.columns(3)
                for idx, category in enumerate(categories):
                    with cols[idx % 3]:
                        with st.container(border=True):
                            st.subheader(category['name'])
                            st.caption(f"ID: {category['id']}")
            else:
                st.info("No categories found. Create one to get started!")
        except Exception as e:
            st.error(f"Error fetching categories: {str(e)}")

    # Create Category
    with tab2:
        st.subheader("Create a New Category")
        with st.form("create_category_form"):
            name = st.text_input("Category Name *")
            submitted = st.form_submit_button("Create Category")

            if submitted:
                if name:
                    try:
                        category_data = {"name": name}
                        response = requests.post(f"{API_URL}/categories/", json=category_data)
                        if response.status_code == 200:
                            st.success("Category created successfully!")
                            st.json(response.json())
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error creating category: {str(e)}")
                else:
                    st.error("Please enter a category name")

    # Update Category
    with tab3:
        st.subheader("Update a Category")
        try:
            response = requests.get(f"{API_URL}/categories/")
            categories = response.json()
            category_options = {f"{c['id']} - {c['name']}": c['id'] for c in categories}

            if category_options:
                selected_category = st.selectbox("Select Category to Update", category_options.keys())
                category_id = category_options[selected_category]
                current_category = next(c for c in categories if c['id'] == category_id)

                with st.form("update_category_form"):
                    name = st.text_input("Category Name", value=current_category['name'])
                    submitted = st.form_submit_button("Update Category")

                    if submitted:
                        if name:
                            try:
                                category_data = {"name": name}
                                response = requests.put(f"{API_URL}/categories/{category_id}", json=category_data)
                                if response.status_code == 200:
                                    st.success("Category updated successfully!")
                                    st.json(response.json())
                                else:
                                    st.error(f"Error: {response.text}")
                            except Exception as e:
                                st.error(f"Error updating category: {str(e)}")
                        else:
                            st.error("Please enter a category name")
            else:
                st.info("No categories available to update")
        except Exception as e:
            st.error(f"Error loading categories: {str(e)}")

    # Delete Category
    with tab4:
        st.subheader("Delete a Category")
        try:
            response = requests.get(f"{API_URL}/categories/")
            categories = response.json()
            category_options = {f"{c['id']} - {c['name']}": c['id'] for c in categories}

            if category_options:
                selected_category = st.selectbox("Select Category to Delete", category_options.keys())
                category_id = category_options[selected_category]

                if st.button("Delete Category", type="secondary"):
                    try:
                        response = requests.delete(f"{API_URL}/categories/{category_id}")
                        if response.status_code == 200:
                            st.success("Category deleted successfully!")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error deleting category: {str(e)}")
            else:
                st.info("No categories available to delete")
        except Exception as e:
            st.error(f"Error loading categories: {str(e)}")

