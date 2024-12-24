import streamlit as st

login = st.Page("login.py", title = "Login", default = True)
cookbot = st.Page("cookbot.py", title= "workout", )

pg = st.navigation([login, cookbot])
st.set_page_config(page_title="Document", page_icon=":material/edit:")
pg.run()