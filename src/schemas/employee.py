from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreateSchema(BaseModel):
    """Схема для создания сотрудника"""
    model_config = ConfigDict(extra="forbid")

    id_telegram: int = Field(title="Telegram ID")
    zup_id: str = Field(title="ZUP ID", min_length=1)
    login: str = Field(title="Login", min_length=3)
    first_name: str = Field(title="First Name", min_length=2, max_length=50)
    last_name: str = Field(title="Last Name", min_length=2, max_length=50)
    middle_name: str | None = Field(default=None, title="Middle Name", max_length=50)
    full_name: str = Field(title="Full Name", min_length=2)
    age: int = Field(title="Age", ge=18, le=100)
    date_of_birth: date = Field(title="Date of Birth")
    gender: str = Field(title="Gender", pattern="^(male|female)$")
    position: str = Field(title="Position", min_length=2)
    department: str = Field(title="Department", min_length=2)
    organisation: str = Field(title="Organisation", min_length=2)
    full_org_structure: str = Field(title="Full Organisation Structure")
    date_of_start: date = Field(title="Date of Start")
    date_of_end: date | None = Field(default=None, title="Date of End")
    phone: str = Field(title="Phone", min_length=7, max_length=15)
    email: EmailStr = Field(title="Email")
    is_working: bool = Field(default=True, title="Is Working")


class EmployeeSchema(EmployeeCreateSchema):
    """Схема для отображения сотрудника"""
    model_config = ConfigDict(from_attributes=True)

    id: int


class EmployeeUpdateSchema(BaseModel):
    """Схема для обновления данных сотрудника"""
    model_config = ConfigDict(extra="forbid")

    zup_id: str | None = Field(default=None, title="ZUP ID", min_length=1)
    login: str | None = Field(default=None, title="Login", min_length=3)
    first_name: str | None = Field(default=None, title="First Name", min_length=2, max_length=50)
    last_name: str | None = Field(default=None, title="Last Name", min_length=2, max_length=50)
    middle_name: str | None = Field(default=None, title="Middle Name", max_length=50)
    full_name: str | None = Field(default=None, title="Full Name", min_length=2)
    age: int | None = Field(default=None, title="Age", ge=18, le=100)
    date_of_birth: date | None = Field(default=None, title="Date of Birth")
    gender: str | None = Field(default=None, title="Gender", pattern="^(male|female)$")
    position: str | None = Field(default=None, title="Position", min_length=2)
    department: str | None = Field(default=None, title="Department", min_length=2)
    organisation: str | None = Field(default=None, title="Organisation", min_length=2)
    full_org_structure: str | None = Field(default=None, title="Full Organisation Structure")
    date_of_start: date | None = Field(default=None, title="Date of Start")
    date_of_end: date | None = Field(default=None, title="Date of End")
    phone: str | None = Field(default=None, title="Phone", min_length=7, max_length=15)
    email: EmailStr | None = Field(default=None, title="Email")
    is_working: bool | None = Field(default=None, title="Is Working")