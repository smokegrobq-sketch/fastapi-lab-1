import os

from fastapi import FastAPI
from psycopg import connect

app = FastAPI(
    title="FastAPI Lab 1",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "FastAPI template is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/db-health")
def database_health_check() -> dict[str, str]:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return {"database": "not configured"}

    with connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

    return {"database": "ok"}


def start() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
