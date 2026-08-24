# Expense tracker

Expense tracker is a Python project that helps you track daily expenses easily.

## Technical stack
FastAPI, PostgreSQL, SQLAlchemy, Alembic, pytest, Docker

## Setup

1. Copy the example environment file and fill in your own values:
```bash
   cp .env.example .env
```
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Start the PostgreSQL database:
```bash
   docker compose up -d
```
4. Apply database migrations:
```bash
   alembic upgrade head
```
5. Run the API:
```bash
   uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## Tests

```bash
pytest -v
```

Tests run against an isolated in-memory SQLite database and don't affect your local PostgreSQL data.
