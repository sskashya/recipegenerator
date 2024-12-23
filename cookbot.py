import streamlit as st
#import openai
import requests

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
        #st.write(recipes)
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
            #with col3:
                #ing_sub = st.button("Substitute for Ingredients")
            st.write("-" * 40)
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
