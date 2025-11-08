from fastapi import APIRouter, HTTPException
import logging

from ...database import init_db

router = APIRouter(prefix="/admin", tags=["Администрирование"])
logger = logging.getLogger(__name__)


@router.post("/init_db", summary="Инициализация базы данных")
async def initialize_database():
    """Пересоздает все таблицы в БД (удаляет существующие данные)"""
    try:
        logger.info("Получен запрос на инициализацию БД")
        await init_db()
        return {"message": "Database initialized successfully"}
    except Exception as e:
        logger.error(f"Ошибка при инициализации БД через API: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при инициализации БД: {str(e)}"
        )
