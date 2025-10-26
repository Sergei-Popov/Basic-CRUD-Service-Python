from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr

class UserSchema(UserCreateSchema):
    id: int

class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None