from openai import OpenAI
import streamlit as st
import pandas as pd
from datetime import datetime
import openai
import json
import os

if 'username' in st.session_state:
    st.header("Shopping Cart \U0001F6D2")
    file_path = f"grocery_file/prelim_shopping_list_{st.session_state.username}.json"
    with open(file_path, 'r') as f:
        prelim_grocery = json.load(f)
    ingredients_data = []
    st.write(prelim_grocery)
    for recipe in prelim_grocery:
        for ingredient in recipe['ingredients']:   
            ingredients_data.append({
                "username": recipe['username'],
                "recipe_name": recipe['recipe name'],  
                "recipe_id": recipe['recipe id'],
                "ingredient": ingredient,
                "picked_up": False  
            })

    editable_data = st.data_editor(
        ingredients_data,
        column_config={
            "ingredient": st.column_config.TextColumn("Ingredient"),
            "picked_up": st.column_config.CheckboxColumn(
                    "In Cart",
                    default=False,
            )
        }
    )

    st.write("-"*40)
    st.subheader("Find Substitutes for Ingredients")
    col3, col4 = st.columns(2, gap = "medium")
    with col3:
        ingredient = st.text_input("Enter your ingredient here")
    with col4:
        sub = st.button("Generate Alternative Ingredients")
    
    if ingredient and sub:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        messages = [{"role":"system", "content": f"You are a knowledgeable food bot. Provide alternative ingredients for the ingredient provided by the chef. The ingredient provided by the chef is {ingredient}"}]
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages = messages,
                stream = True,
                temperature = 0
                )
        st.write_stream(response)
    st.write("-"*40)
    col1, col2 = st.columns(2, gap = "medium")
    with col1:
        save_list = st.button("Save", icon = '\U0001F6D2')
    with col2:
        clear_list = st.button("Clear Cart", icon = '\U0001F5D1')

    if save_list:
        editable_data.to_csv("recipes.csv", index=False)
        st.success("Grocery List has been saved!")
    if clear_list:
        data = pd.DataFrame(columns=["username", "date", "recipe name", "recipe id", "ingredients", "In Cart"])
        st.session_state["data_editor"] = data
        st.experimental_rerun()
    
    logout = st.button("Logout")
    if logout:
        st.session_state.username = None
else:
    st.warning("Please login to continue")