import streamlit as st
import time
from utils.db import init_db
from auth import AuthManager

init_db()

st.title("AI Hisobchi")
st.write("AI powered finance tracker.")

auth = AuthManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.user_id = None

tab1, tab2 = st.tabs(["🔑 Login", "➕ Register"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        user_id = auth.login_user(email, password)
        if user_id is not None:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.user_id = user_id
            st.success("Login successful, redirecting...")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Invalid email or password.")

with tab2:
    st.subheader("Register")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    register_btn = st.button("Register")

    if register_btn:
        if auth.register_user(new_email, new_password):
            st.success("Registration successful! Please log in.")
        else:
            st.error("Email already exists.")

if st.session_state.logged_in:
    st.success("Head to the sidebar to use features")
    st.toast("Welcome to Finance Tracker App!")
