import os
from dotenv import load_dotenv
import cohere

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)


def get_budget_insights(user_query, transactions_text):
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return "❌ API Key missing."

    try:
        co = cohere.Client(api_key)

        system_message = (
            "You are FinanceBot, a financial AI assistant. "
            "Assist users ONLY with financial queries (budgeting, tracking). "
            "If asked about yourself, say you were built by Jamshid"
        )

        response = co.chat(
            model="command-r-08-2024",  # This is the current stable version
            message=f"User query: {user_query}\n\nRecent Transactions:\n{transactions_text}",
            preamble=system_message,
        )

        return response.text

    except Exception as e:
        return f"❌ Bot Error: {str(e)}"
