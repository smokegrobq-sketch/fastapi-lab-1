from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.categories import router as categories_router
from app.api.me import router as me_router
from app.api.orders import router as orders_router
from app.api.products import router as products_router
from app.api.profiles import router as profiles_router
from app.api.users import router as users_router
from app.db.session import async_session_factory


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Lab",
        version="0.3.0",
    )

    app.include_router(auth_router)
    app.include_router(me_router)
    app.include_router(users_router)
    app.include_router(profiles_router)
    app.include_router(categories_router)
    app.include_router(products_router)
    app.include_router(orders_router)

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"message": "FastAPI template is running"}

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/db-health")
    async def database_health_check() -> dict[str, str]:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))

        return {"database": "ok"}

    return app
