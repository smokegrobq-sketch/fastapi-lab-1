# FastAPI Lab 1

Template project for a FastAPI application managed with Poetry.

## Requirements

- Python 3.11+
- Poetry

## Install

```bash
poetry install
```

## Run

```bash
poetry run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to view the generated API documentation.

## Test

```bash
poetry run pytest
```

## Run With Docker

```bash
docker compose up --build
```

The FastAPI container uses auto reload and mounts the project folder into
`/app`, so code changes on the host are reflected inside the container.

Useful URLs:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/db-health`

## Users CRUD

User data is stored in PostgreSQL through async SQLAlchemy sessions.

Available endpoints:

- `GET /users/`
- `GET /users/{user_id}`
- `POST /users/`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

## Database Models

The project uses PostgreSQL, async SQLAlchemy and Alembic migrations.

Models:

- `User`
- `Profile`
- `Category`
- `Product`
- `Order`
- `OrderItem`

Relationships:

- `User` one-to-one `Profile`
- `User` one-to-many `Order`
- `Category` one-to-many `Product`
- `Order` one-to-many `OrderItem`
- `Product` one-to-many `OrderItem`

Run migrations manually:

```bash
poetry run alembic upgrade head
```

When running with Docker Compose, migrations run before the FastAPI server starts.
