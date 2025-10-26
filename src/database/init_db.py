from .models import Base
from .session import engine


async def init_db() -> None:
    """Пересоздать все таблицы в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)