import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from utils.expenseTracker import Account


@pytest.fixture
def account_with_mocks():
    with patch("utils.expenseTracker.ExpenseManager") as MockExpense, \
         patch("utils.expenseTracker.IncomeManager") as MockIncome, \
         patch("streamlit.success"), \
         patch("streamlit.warning"):
        expense_mgr = MockExpense.return_value
        income_mgr = MockIncome.return_value
        account = Account(user_id=1)
        yield account, expense_mgr, income_mgr


class TestAccountBalance:

    def test_get_balance_calculates_correctly(self, account_with_mocks):
        account, expense_mgr, income_mgr = account_with_mocks
        income_mgr.viewIncome.return_value = pd.DataFrame({"amount": [1000.0, 500.0]})
        expense_mgr.viewExpenses.return_value = pd.DataFrame({"amount": [200.0, 300.0]})

        assert account.getBalance() == 1000.0  # 1500 - 500

    def test_get_balance_no_transactions(self, account_with_mocks):
        account, expense_mgr, income_mgr = account_with_mocks
        income_mgr.viewIncome.return_value = pd.DataFrame({"amount": pd.Series([], dtype=float)})
        expense_mgr.viewExpenses.return_value = pd.DataFrame({"amount": pd.Series([], dtype=float)})

        assert account.getBalance() == 0.0


class TestAccountDeleteExpense:

    def test_delete_valid_id_adjusts_balance(self, account_with_mocks):
        account, expense_mgr, _ = account_with_mocks
        account.Balance = 500.0
        expense_mgr.viewExpenses.return_value = pd.DataFrame({"id": [1, 2], "amount": [100.0, 200.0]})

        account.deleteExpense(expense_id=1)

        expense_mgr.deleteExpense.assert_called_once_with(1)
        assert account.Balance == 600.0

    def test_delete_invalid_id_does_nothing(self, account_with_mocks):
        account, expense_mgr, _ = account_with_mocks
        expense_mgr.viewExpenses.return_value = pd.DataFrame({"id": [1, 2], "amount": [100.0, 200.0]})

        account.deleteExpense(expense_id=99)

        expense_mgr.deleteExpense.assert_not_called()

    def test_delete_when_empty_does_nothing(self, account_with_mocks):
        account, expense_mgr, _ = account_with_mocks
        expense_mgr.viewExpenses.return_value = pd.DataFrame(
            {"id": pd.Series([], dtype=int), "amount": pd.Series([], dtype=float)}
        )

        account.deleteExpense(expense_id=1)

        expense_mgr.deleteExpense.assert_not_called()


class TestAccountDeleteIncome:

    def test_delete_valid_id_adjusts_balance(self, account_with_mocks):
        account, _, income_mgr = account_with_mocks
        account.Balance = 500.0
        income_mgr.viewIncome.return_value = pd.DataFrame({"id": [1, 2], "amount": [100.0, 200.0]})

        account.deleteIncome(income_id=1)

        income_mgr.deleteIncome.assert_called_once_with(1)
        assert account.Balance == 400.0

    def test_delete_invalid_id_does_nothing(self, account_with_mocks):
        account, _, income_mgr = account_with_mocks
        income_mgr.viewIncome.return_value = pd.DataFrame({"id": [1], "amount": [100.0]})

        account.deleteIncome(income_id=99)

        income_mgr.deleteIncome.assert_not_called()

    def test_delete_when_empty_does_nothing(self, account_with_mocks):
        account, _, income_mgr = account_with_mocks
        income_mgr.viewIncome.return_value = pd.DataFrame(
            {"id": pd.Series([], dtype=int), "amount": pd.Series([], dtype=float)}
        )

        account.deleteIncome(income_id=1)

        income_mgr.deleteIncome.assert_not_called()


class TestAccountFormatForAI:

    def test_format_transactions_for_ai_shape(self, account_with_mocks):
        account, expense_mgr, income_mgr = account_with_mocks
        expense_mgr.viewExpenses.return_value = pd.DataFrame({
            "name": ["Groceries"], "date": ["2024-01-15"], "amount": [50.0],
            "category": ["Food"], "description": ["Weekly shopping"],
        })
        income_mgr.viewIncome.return_value = pd.DataFrame({
            "name": ["Salary"], "date": ["2024-01-01"], "amount": [3000.0],
            "source": ["Employer"], "description": ["Monthly pay"],
        })

        result = account.format_transactions_for_ai()

        assert set(result.keys()) == {"income", "expenses"}
        assert result["income"][0]["name"] == "Salary"
        assert result["expenses"][0]["name"] == "Groceries"

    def test_format_transactions_for_ai_empty(self, account_with_mocks):
        account, expense_mgr, income_mgr = account_with_mocks
        expense_mgr.viewExpenses.return_value = pd.DataFrame(
            columns=["name", "date", "amount", "category", "description"]
        )
        income_mgr.viewIncome.return_value = pd.DataFrame(
            columns=["name", "date", "amount", "source", "description"]
        )

        result = account.format_transactions_for_ai()

        assert result["income"] == []
        assert result["expenses"] == []
