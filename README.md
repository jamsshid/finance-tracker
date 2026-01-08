# finance-tracker

Finance Tracker is a web application built with Streamlit that helps users manage their personal finances. It provides features for logging income and expenses, viewing detailed transaction history, and generating insightful financial reports. The application also includes an AI-powered chatbot to answer financial questions and provide budget advice based on user data.

## Features

- **User Authentication:** Secure user registration and login system.
- **Transaction Management:** Easily add, view, and delete income and expense records.
- **Dynamic Balance:** The current account balance is displayed and updated in real-time.
- **Financial Reports:** Interactive visualizations of financial data, including:
  - Expense breakdown by category (Pie Chart).
  - Income breakdown by source (Pie Chart).
  - Monthly income vs. expense trends (Area & Stacked Bar Charts).
- **AI Finance Bot:** A chatbot integrated with Cohere's API to provide personalized financial insights and advice based on your transaction history.
- **Personalized Data Storage:** Each user's financial data is stored in a separate, dedicated SQLite database for privacy.

## Technologies Used

- **Framework:** Streamlit
- **Database:** SQLite3
- **Data Manipulation:** Pandas
- **Data Visualization:** Plotly
- **AI/LLM:** Cohere

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.8+
- A Cohere API key

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/jamsshid/finance-tracker.git
    cd finance-tracker
    ```

2.  **Install the required Python packages:**
    ```sh
    pip install streamlit pandas plotly-express cohere python-dotenv
    ```

3.  **Set up your environment variables:**
    - Create a file named `.env` in the root directory of the project.
    - Add your Cohere API key to this file:
      ```
      COHERE_API_KEY='your_cohere_api_key_here'
      ```

### Running the Application

1.  Execute the following command in your terminal from the project's root directory:
    ```sh
    streamlit run home.py
    ```

2.  The application will open in your web browser. You can register a new account or log in if you already have one.

## Project Structure

```
.
├── home.py                # Main application file, handles login/registration
├── auth.py                # Manages user authentication logic (registration, login)
├── pages/
│   ├── report.py          # Generates financial reports and hosts the AI bot
│   ├── transaction_log.py # Page for adding new income/expenses
│   └── view_transactions.py # Page for viewing and deleting existing transactions
└── utils/
    ├── expenseTracker.py  # Core logic for managing accounts, income, and expenses
    └── financebot.py      # Handles communication with the Cohere API for the AI assistant
