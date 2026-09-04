# Finance-Tracker

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
- **Multi-user support:** All user data is isolated by user ID in a shared PostgreSQL database.

## Technologies Used

- **Framework:** Streamlit
- **Database:** PostgreSQL (psycopg2-binary)
- **Data Manipulation:** Pandas
- **Data Visualization:** Plotly
- **AI/LLM:** Cohere
- **Containerization:** Docker & Docker Compose

## Getting Started

### Prerequisites

- A Cohere API key — https://dashboard.cohere.com/api-keys
- **Docker route:** Docker Desktop (recommended)
- **Local route:** Python 3.10+, PostgreSQL 14+

---

### Option A — Docker (recommended)

No local PostgreSQL installation required. PostgreSQL data persists in a named Docker volume.

1. Clone the repository:
   ```sh
   git clone https://github.com/jamsshid/finance-tracker.git
   cd finance-tracker
   ```

2. Set up environment variables:
   ```sh
   copy .env.example .env       # Windows
   # cp .env.example .env       # macOS/Linux
   ```
   Edit `.env` and set your `COHERE_API_KEY`. The default `DATABASE_URL` and `POSTGRES_PASSWORD` already match the Compose service — change them only if needed.

3. Build and start all services:
   ```sh
   docker compose up --build
   ```
   Tables are created automatically on first startup.

4. Open **http://localhost:8501** in your browser.

**Useful commands:**
```sh
docker compose up -d          # Run in background
docker compose down           # Stop and remove containers
docker compose down -v        # Stop and also delete the database volume
docker compose logs -f app    # Stream app logs
```

---

### Option B — Local (manual setup)

1. Clone the repository:
   ```sh
   git clone https://github.com/jamsshid/finance-tracker.git
   cd finance-tracker
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE finance_tracker;
   ```

5. Set up environment variables:
   ```sh
   copy .env.example .env       # Windows
   # cp .env.example .env       # macOS/Linux
   ```
   Edit `.env`: set `DATABASE_URL` to use `localhost` as the host (see the commented example in `.env.example`) and fill in your `COHERE_API_KEY`.

6. Run the app — tables are created automatically on first startup:
   ```sh
   streamlit run home.py
   ```

## Testing

Unit tests cover `ExpenseManager`, `IncomeManager`, and `Account` using mocked database connections — no running database required.

```sh
pytest
```

Tests live in `tests/` and are discovered automatically via `pytest.ini`. The mock fixture in `tests/conftest.py` stubs the PostgreSQL connection so tests run in isolation.

## Project Structure

```
.
├── home.py                # Entry point — login/register, DB initialization
├── auth.py                # User authentication (register, login)
├── pages/
│   ├── report.py          # Financial reports and AI chatbot
│   ├── transaction_log.py # Add income and expenses
│   └── view_transactions.py # View and delete transactions
├── utils/
│   ├── db.py              # PostgreSQL connection factory and schema init
│   ├── expenseTracker.py  # ExpenseManager, IncomeManager, Account classes
│   └── financebot.py      # Cohere API wrapper for financial insights
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```
