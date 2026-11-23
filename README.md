# Expense tracker

Expense tracker is a Python project that helps you track daily expenses easily.

## Technical stack
FastAPI, PostgreSQL, SQLAlchemy, Alembic, pytest, Docker

## Setup

1. Copy the example environment file and fill in your own values:
```bash
   cp .env.example .env
```
2. Start the API and PostgreSQL database:
```bash
   docker compose up -d --build
```
3. Apply database migrations:
```bash
   docker compose exec api alembic upgrade head
```
4. Check the API liveness:
```bash
   curl http://localhost:8080/health
```
the /health endpoint checks that the API is running.
5. Check the API readiness:
```bash
   curl http://localhost:8080/ready
```
the /ready endpoint checks that the API is ready to serve traffic by verifying that the database responds.

The API is available at `http://localhost:8080`.
Interactive API documentation is available at `http://localhost:8080/docs`.

To view API logs:
```bash
   docker compose logs -f api
```
To stop the application:
```bash
   docker compose down
```