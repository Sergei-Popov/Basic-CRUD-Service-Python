from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    """Схема для создания пользователя"""
    model_config = ConfigDict(extra="forbid")

    id_telegram: int = Field(title="Telegram ID")
    username: str | None = Field(default=None, title="Username", min_length=3, max_length=30)
    first_name: str = Field(title="First Name", min_length=2, max_length=50)
    last_name: str | None = Field(default=None, title="Last Name", min_length=2, max_length=50)

class UserSchema(UserCreateSchema):
    """Схема для отображения пользователя"""
    id: int
    phone_number: str | None = Field(default=None, title="Phone Number", min_length=7, max_length=12)

class UserUpdateSchema(BaseModel):
    """Схема для обновления данных пользователя"""
    model_config = ConfigDict(extra="forbid")

    username: str | None = Field(default=None, title="Username", min_length=3, max_length=30)
    first_name: str | None = Field(default=None, title="First Name", min_length=2, max_length=50)
    last_name: str | None = Field(default=None, title="Last Name", min_length=2, max_length=50)
    phone_number: str | None = Field(default=None, title="Phone Number", min_length=7, max_length=12)