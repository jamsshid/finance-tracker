import streamlit as st
import sqlite3
import time
from utils.expenseTracker import ExpenseManager
from utils.expenseTracker import IncomeManager
from utils.expenseTracker import Account
from auth import AuthManager

st.title("AI Hisobchi")
st.write("AI powered finance tracker.")

auth = AuthManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

tab1, tab2 = st.tabs(["🔑 Login","➕ Register"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password",type="password")
    login_btn = st.button("Login")

    if login_btn:
        if auth.login_user(email,password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login successful redirecting...")
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
        if auth.register_user(new_email,new_password):
            st.success("Registration succesful! Please log in.")
        else:
            st.error("Email already exists.")

if st.session_state.logged_in:

    st.success("Head to side bar to use features")

db_name = "expenses.db"

ExManager = ExpenseManager(db_name=db_name)
InManager = IncomeManager(db_name=db_name)
account = Account(db_name=db_name)

conn = sqlite3.connect(db_name)
c=conn.cursor()

if st.session_state.logged_in:

    st.toast("Welcome to Finance Tracker App!")

conn.close()


