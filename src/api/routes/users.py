from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from ...database import UserModel
from ...schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from ..dependencies import SessionDep

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/", summary="Создание нового пользователя")
async def create_user(user: UserCreateSchema, session: SessionDep):
    """Создает нового пользователя в БД"""
    new_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {
        "status": "success",
        "message": "User created",
        "user_id": new_user.id,
    }


@router.get("/", response_model=list[UserSchema], summary="Получение списка всех пользователей")
async def get_users(session: SessionDep) -> list[UserSchema]:
    """Возвращает список всех пользователей"""
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserSchema, summary="Получение пользователя по ID")
async def get_user(user_id: int, session: SessionDep) -> UserSchema:
    """Возвращает пользователя по ID"""
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", summary="Удаление пользователя")
async def delete_user(user_id: int, session: SessionDep):
    """Удаляет пользователя из БД"""
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"status": "success", "message": "User deleted"}


@router.patch("/{user_id}", summary="Обновление пользователя")
async def update_user(user_id: int, user_update: UserUpdateSchema, session: SessionDep):
    """Обновляет данные пользователя"""
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.first_name is not None:
        user.first_name = user_update.first_name
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
    if user_update.email is not None:
        user.email = user_update.email

    session.add(user)
    await session.commit()
    return {"status": "success", "message": "User updated"}