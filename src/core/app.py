from contextlib import asynccontextmanager

from fastapi import FastAPI

from ..api.routes import admin_router, users_router
from ..database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    """Создает и настраивает FastAPI приложение"""
    app = FastAPI(
        title="Basic CRUD Service",
        lifespan=lifespan,
    )

    # Регистрация роутеров
    app.include_router(admin_router)
    app.include_router(users_router)

    return app