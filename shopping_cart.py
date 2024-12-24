from openai import OpenAI
import streamlit as st
import pandas as pd
import datetime
import openai
import json
import os

if st.session_state.username:
    st.header("Shopping Cart \U0001F6D2")
    file_path: f"grocery_file/prelim_shopping_list_{st.session_state.username}.json"
    prelim_grocery = json.load(f"grocery_file/prelim_shopping_list_{st.session_state.username}.json")
    editable_data = st.data_editor(
        prelim_grocery,
        column_config={
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
    
    if col3 and col4:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        messages = {"role":"system", "content": f"You are a knowledgeable food bot. Provide alternative ingredients for the ingredient provided by the chef. The ingredient provided by the chef is {col3}"}
        response = client.chat.completions.create(
                model="gpt-4o",
                messages = messages,
                stream = True,
                temperature = 0
                )

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
    
    logout = st.button("Logout")
    if logout:
        st.session_state.username = None
else:
    st.warning("Please login to continue")