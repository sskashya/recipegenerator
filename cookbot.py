import streamlit as st
#import openai
import requests
import json
import os
import datetime

api_key = st.secrets['SPOON_API_KEY']
openai_client = st.secrets['OPENAI_API_KEY']

def findbyingredients(ingredients = []):
    url = "https://api.spoonacular.com/recipes/findByIngredients"

    params = {
        "ingredients": ingredients,
        "number": 5,  
        "apiKey": api_key
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()
        st.write(recipes[0])
        for recipe in recipes:
            st.image(f"{recipe['image']}")
            st.write(f"Recipe: {recipe['title']}")
            st.write(f"ID: {recipe['id']}")
            st.write(f" Ingredients: {recipe['usedIngredients']['originalName']}, ", args = list)
            st.write("-" * 40)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def ingredient_sub(ingredient_name):
    url = "https://api.spoonacular.com/food/ingredients/substitutes"
    params = {
        "ingredients": ingredient_name,
        "apiKey": api_key 
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        subs = response.json()
        st.write(f"{subs['id']}, {subs['ingredient']}")
        st.write(f"Substitutes: {subs['substitutes']}", args = list)
        print("-" * 40)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def recipe_search(prompt, number = 5, diet = None, exclude_ingredients = None, intolerances = None, offset = None):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": prompt,
        "number": number,
        "diet": diet,
        "excludeIngredients": exclude_ingredients,
        "intolerances": intolerances,
        "fillIngredients": True,
        "addRecipeInformation": True,
        "addRecipeInstructions": True,
        "ignorePantry": False,
        "offset": offset,
        "apiKey":api_key
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()
        for recipe in recipes['results']:
            st.header(f"Recipe: {recipe['title']}")
            st.write(f"ID: {recipe['id']}")
            st.image(f"{recipe['image']}")
            if st.button:
                expanded_recipe = st.expander("More Information")
                expanded_recipe.write("-" * 40)
                expanded_recipe.subheader(f"Servings: {recipe['servings']}")
                for ingredient in recipe['missedIngredients']:
                    expanded_recipe.write(f" - {ingredient['original']}")
                expanded_recipe.write("-" * 40)
                for instructions in recipe['analyzedInstructions']:
                    if instructions['name'] == "":
                        expanded_recipe.subheader(f"Prep\n ")
                    else:
                        expanded_recipe.subheader(f"{instructions['name']}\n ")
                    for steps in instructions['steps']:
                        expanded_recipe.write(f" Step: {steps['number']}\n - {steps['step']}\n ")
            col1, col2 = st.columns(2, gap = 'medium')
            with col1:
                save_recipe = st.button("Save", icon = '\U0001F4BE', key = recipe['id'])
            with col2:
                shopping_cart = st.button("Add to Grocery List", icon = '\U0001F6D2', key = recipe['title'])
            st.write("-" * 40)
            if save_recipe:
                os.makedirs('file', exist_ok=True)
                log_file = f"file/recipe_hist_{st.session_state.username}.json"

                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        try:
                            memories = json.load(f)
                        except json.JSONDecodeError:
                            memories = []
                else:
                    memories = []
                for recipe in recipes:
                    recipe_hist = {
                        "username": st.session_state.username,
                        "date": datetime.now().date(),
                        "recipe name": recipe['title'],
                        "recipe id": recipe['id']
                    }

                    memories = [
                        memory for memory in memories
                        if not (
                            memory['recipe id'] == recipe_hist['recipe id'] and
                            memory['date'] == recipe_hist['date']
                        )
                    ]
                    memories.append(recipe_hist)

                with open(log_file, 'w') as f:
                    json.dump(memories, f, indent=2)
                st.success("Recipe successfully saved!")

            
            if shopping_cart:
                os.makedirs('grocery_file', exist_ok=True)
                log_file = f"grocery_file/prelim_shopping_list_{st.session_state.username}.json"

                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        try:
                            groceries = json.load(f)
                        except json.JSONDecodeError:
                            groceries = []
                else:
                    groceries = []
                for recipe in recipes:
                    grocery_list = {
                        "recipe name": recipe['title'],
                        "recipe id": recipe['id'],
                        "ingredients": [ingredient['name'] for ingredient in recipe['missedIngredients']]
                    }

                    memories = [
                        memory for memory in memories
                        if not (
                            groceries['recipe id'] == grocery_list['recipe id'] and
                            groceries['recipe name'] == grocery_list['recipe name']
                        )
                    ]
                    memories.append(grocery_list)

                with open(log_file, 'w') as f:
                    json.dump(memories, f, indent=2)
                st.success("Ingredients added to Shopping List!")


    else:
        st.warning(f"Error: {response.status_code}")
        st.warning(response.text)

def food_joke():
    url = "https://api.spoonacular.com/food/jokes/random"
    params = {"apiKey": api_key}
    response = requests.get(url, params = params)

    if response.status_code == 200:
        joke = response.json()
        st.write(joke['text'], color = "blue")
        st.write("_" * 40)
    else:
        st.warning(f"Error: {response.status_code}")
        st.warning(response.text)

if st.session_state.username:
    st.title("Welcome Back!")
    st.header("Here is your food joke of the day")

    food_joke()
    st.write("-"*40)

    search = st.text_input("Search for meals here")
    if search:
        diet = st.selectbox("Select your Diet Option", ["None", "Gluten Free", "Pescetarian", "Vegan", "Vegetarian", "Ketogenic"])
        if diet != 'None':
            recipe_search(search, diet = diet)
        
        else:
            recipe_search(search)




    logout = st.button("Logout")
    if logout:
        st.session_state.username = None

else:
    st.warning("Please login to continue")
