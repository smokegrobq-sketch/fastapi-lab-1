import os

from fastapi import FastAPI
from psycopg import connect

from app.api.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Lab",
        version="0.3.0",
    )

    app.include_router(users_router)

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

    return app
