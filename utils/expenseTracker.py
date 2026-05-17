import pandas as pd
import streamlit as st
from utils.db import get_connection


class ExpenseManager:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def addExpense(self, date, name, amount, category, description):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO expenses (user_id, name, date, amount, category, description) VALUES (%s,%s,%s,%s,%s,%s)",
                    (self.user_id, name, date, amount, category, description),
                )
            conn.commit()
        finally:
            conn.close()

    def viewExpenses(self) -> pd.DataFrame:
        conn = get_connection()
        try:
            return pd.read_sql_query(
                "SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC",
                conn,
                params=(self.user_id,),
            )
        finally:
            conn.close()

    def deleteExpense(self, expense_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM expenses WHERE id = %s AND user_id = %s",
                    (expense_id, self.user_id),
                )
            conn.commit()
        finally:
            conn.close()


class IncomeManager:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def addIncome(self, date, name, amount, source, description):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO income (user_id, name, date, amount, source, description) VALUES (%s,%s,%s,%s,%s,%s)",
                    (self.user_id, name, date, amount, source, description),
                )
            conn.commit()
        finally:
            conn.close()

    def viewIncome(self) -> pd.DataFrame:
        conn = get_connection()
        try:
            return pd.read_sql_query(
                "SELECT * FROM income WHERE user_id = %s ORDER BY date DESC",
                conn,
                params=(self.user_id,),
            )
        finally:
            conn.close()

    def deleteIncome(self, income_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM income WHERE id = %s AND user_id = %s",
                    (income_id, self.user_id),
                )
            conn.commit()
        finally:
            conn.close()


class Account:

    def __init__(self, user_id: int):
        self.IncomeManager = IncomeManager(user_id)
        self.ExpenseManager = ExpenseManager(user_id)
        self.Balance = 0.0

    def getBalance(self) -> float:
        total_income = self.IncomeManager.viewIncome()["amount"].sum()
        total_expense = self.ExpenseManager.viewExpenses()["amount"].sum()
        self.Balance = float(total_income - total_expense)
        return self.Balance

    def addExpense(self, date, name, amount, category, description):
        self.ExpenseManager.addExpense(date, name, amount, category, description)
        self.Balance -= amount
        st.success("Expense added successfully!")

    def addIncome(self, date, name, amount, source, description):
        self.IncomeManager.addIncome(date, name, amount, source, description)
        self.Balance += amount
        st.success("Income added successfully!")

    def expenseList(self) -> pd.DataFrame:
        return self.ExpenseManager.viewExpenses()

    def incomeList(self) -> pd.DataFrame:
        return self.IncomeManager.viewIncome()

    def deleteExpense(self, expense_id: int):
        expenses = self.ExpenseManager.viewExpenses()
        if expenses.empty:
            st.warning("No expenses to delete.")
            return
        if expense_id in expenses["id"].values:
            amount = expenses.loc[expenses["id"] == expense_id, "amount"].iloc[0]
            self.ExpenseManager.deleteExpense(expense_id)
            self.Balance += float(amount)
            st.success(f"Expense {expense_id} deleted successfully!")
        else:
            st.warning(f"Invalid Expense ID: {expense_id}")

    def deleteIncome(self, income_id: int):
        incomes = self.IncomeManager.viewIncome()
        if incomes.empty:
            st.warning("No income records to delete.")
            return
        if income_id in incomes["id"].values:
            amount = incomes.loc[incomes["id"] == income_id, "amount"].iloc[0]
            self.IncomeManager.deleteIncome(income_id)
            self.Balance -= float(amount)
            st.success(f"Income {income_id} deleted successfully!")
        else:
            st.warning(f"Invalid Income ID: {income_id}")

    def format_transactions_for_ai(self) -> dict:
        expenses = self.ExpenseManager.viewExpenses()
        incomes = self.IncomeManager.viewIncome()
        return {
            "income": incomes[["name", "date", "amount", "source", "description"]].to_dict(orient="records"),
            "expenses": expenses[["name", "date", "amount", "category", "description"]].to_dict(orient="records"),
        }
