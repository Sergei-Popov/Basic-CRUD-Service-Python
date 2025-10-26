from fastapi import APIRouter

from ...database import init_db

router = APIRouter(prefix="/admin", tags=["Администрирование"])


@router.post("/init_db", summary="Инициализация базы данных")
async def initialize_database():
    """Пересоздает все таблицы в БД (удаляет существующие данные)"""
    await init_db()
    return {"message": "Database initialized"}