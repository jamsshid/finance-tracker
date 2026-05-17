import pandas as pd
import pytest
from unittest.mock import patch
from utils.expenseTracker import IncomeManager


class TestIncomeManager:

    def test_add_income_executes_correct_sql(self, db_conn):
        conn, cur = db_conn
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            manager = IncomeManager(user_id=1)
            manager.addIncome("2024-01-01", "Salary", 3000.0, "Employer", "Monthly pay")

        cur.execute.assert_called_once()
        sql, params = cur.execute.call_args[0]
        assert "INSERT INTO income" in sql
        assert params == (1, "Salary", "2024-01-01", 3000.0, "Employer", "Monthly pay")
        conn.commit.assert_called_once()

    def test_view_income_returns_dataframe(self, db_conn):
        conn, _ = db_conn
        expected = pd.DataFrame({
            "id": [1], "user_id": [1], "name": ["Salary"],
            "date": ["2024-01-01"], "amount": [3000.0],
            "source": ["Employer"], "description": ["Monthly pay"],
        })
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            with patch("pandas.read_sql_query", return_value=expected):
                result = IncomeManager(user_id=1).viewIncome()

        assert isinstance(result, pd.DataFrame)
        assert result.iloc[0]["name"] == "Salary"
        assert result.iloc[0]["amount"] == 3000.0

    def test_view_income_empty(self, db_conn):
        conn, _ = db_conn
        empty = pd.DataFrame(columns=["id", "user_id", "name", "date", "amount", "source", "description"])
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            with patch("pandas.read_sql_query", return_value=empty):
                result = IncomeManager(user_id=1).viewIncome()

        assert result.empty

    def test_delete_income_executes_correct_sql(self, db_conn):
        conn, cur = db_conn
        with patch("utils.expenseTracker.get_connection", return_value=conn):
            IncomeManager(user_id=1).deleteIncome(income_id=3)

        cur.execute.assert_called_once()
        sql, params = cur.execute.call_args[0]
        assert "DELETE FROM income" in sql
        assert params == (3, 1)
        conn.commit.assert_called_once()
