import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError, ProgrammingError

from .models import Base
from .session import engine
from ..config import settings

logger = logging.getLogger(__name__)


async def ensure_database_exists() -> None:
    """Проверить существование БД и создать её при необходимости"""
    # Подключаемся к служебной базе postgres
    postgres_url = (
        f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/postgres"
    )

    temp_engine = create_async_engine(
        postgres_url,
        isolation_level="AUTOCOMMIT",
        echo=False,
    )

    try:
        async with temp_engine.connect() as conn:
            # Проверяем, существует ли база данных
            result = await conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": settings.postgres_db}
            )
            exists = result.scalar()

            if not exists:
                # Создаём базу данных
                await conn.execute(text(f"CREATE DATABASE {settings.postgres_db}"))
                logger.info(f"База данных '{settings.postgres_db}' успешно создана")
                print(f"База данных '{settings.postgres_db}' успешно создана")
            else:
                logger.info(f"База данных '{settings.postgres_db}' уже существует")
                print(f"База данных '{settings.postgres_db}' уже существует")
    except (OperationalError, ProgrammingError) as e:
        logger.error(f"Ошибка при проверке/создании БД: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при работе с БД: {e}")
        raise
    finally:
        await temp_engine.dispose()


async def init_db() -> None:
    """Пересоздать все таблицы в БД"""
    try:
        # Сначала убедимся, что база данных существует
        logger.info("Начало инициализации БД...")
        await ensure_database_exists()

        # Затем пересоздаём таблицы
        logger.info("Пересоздание таблиц...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Инициализация БД завершена успешно")
    except Exception as e:
        logger.error(f"Ошибка при инициализации БД: {e}", exc_info=True)
        raise
