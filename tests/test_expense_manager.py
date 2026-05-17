import pandas as pd
import pytest
from unittest.mock import patch
from utils.expenseTracker import ExpenseManager


class TestExpenseManager:

    def test_add_expense_executes_correct_sql(self, db_conn):
        conn, cur = db_conn
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            manager = ExpenseManager(user_id=1)
            manager.addExpense("2024-01-15", "Groceries", 50.0, "Food", "Weekly shopping")

        cur.execute.assert_called_once()
        sql, params = cur.execute.call_args[0]
        assert "INSERT INTO expenses" in sql
        assert params == (1, "Groceries", "2024-01-15", 50.0, "Food", "Weekly shopping")
        conn.commit.assert_called_once()

    def test_view_expenses_returns_dataframe(self, db_conn):
        conn, _ = db_conn
        expected = pd.DataFrame({
            "id": [1], "user_id": [1], "name": ["Groceries"],
            "date": ["2024-01-15"], "amount": [50.0],
            "category": ["Food"], "description": ["Weekly shopping"],
        })
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            with patch("pandas.read_sql_query", return_value=expected):
                result = ExpenseManager(user_id=1).viewExpenses()

        assert isinstance(result, pd.DataFrame)
        assert result.iloc[0]["name"] == "Groceries"
        assert result.iloc[0]["amount"] == 50.0

    def test_view_expenses_empty(self, db_conn):
        conn, _ = db_conn
        empty = pd.DataFrame(columns=["id", "user_id", "name", "date", "amount", "category", "description"])
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            with patch("pandas.read_sql_query", return_value=empty):
                result = ExpenseManager(user_id=1).viewExpenses()

        assert result.empty

    def test_delete_expense_executes_correct_sql(self, db_conn):
        conn, cur = db_conn
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            ExpenseManager(user_id=1).deleteExpense(expense_id=5)

        cur.execute.assert_called_once()
        sql, params = cur.execute.call_args[0]
        assert "DELETE FROM expenses" in sql
        assert params == (5, 1)
        conn.commit.assert_called_once()
