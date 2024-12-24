import streamlit as st

login = st.Page("login.py", title = "Login", default = True)
cookbot = st.Page("cookbot.py", title= "CookBot")
cart = st.Page("shopping_cart.py", title = "Shopping Cart")

pg = st.navigation([login, cookbot, cart])
st.set_page_config(page_title="Document", page_icon=":material/edit:")
pg.run()