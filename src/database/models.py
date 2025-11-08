from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_telegram: Mapped[int] = mapped_column(nullable=False, unique=True)
    username: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    phone_number: Mapped[str | None] = mapped_column(nullable=True, unique=True)

    # Связь один-к-одному
    employee: Mapped["EmployeeModel"] = relationship(back_populates="user", uselist=False)

class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_telegram: Mapped[int] = mapped_column(
        ForeignKey("users.id_telegram", ondelete="CASCADE"), 
        nullable=False, 
        unique=True
    )
    zup_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str | None] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)
    department: Mapped[str] = mapped_column(nullable=False)
    organisation: Mapped[str] = mapped_column(nullable=False)
    full_org_structure: Mapped[str] = mapped_column(nullable=False)
    date_of_start: Mapped[date] = mapped_column(nullable=False)
    date_of_end: Mapped[date | None] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    is_working: Mapped[bool] = mapped_column(nullable=False, default=True)

    # Связь один-к-одному
    user: Mapped["UserModel"] = relationship(back_populates="employee")