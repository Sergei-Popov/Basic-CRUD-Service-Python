from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from ...database import EmployeeModel
from ...schemas import EmployeeCreateSchema, EmployeeSchema, EmployeeUpdateSchema
from ..dependencies import SessionDep

router = APIRouter(prefix="/employees", tags=["Сотрудники"])


@router.post("/", summary="Создание нового сотрудника")
async def create_employee(employee: EmployeeCreateSchema, session: SessionDep):
    """Создает нового сотрудника в БД"""
    new_employee = EmployeeModel(**employee.model_dump())
    session.add(new_employee)
    await session.commit()
    await session.refresh(new_employee)
    return {
        "status": "success",
        "message": "Employee created",
        "employee_id": new_employee.id,
    }


@router.get("/", response_model=list[EmployeeSchema], summary="Получение списка всех сотрудников")
async def get_employees(session: SessionDep) -> list[EmployeeSchema]:
    """Возвращает список всех сотрудников"""
    query = select(EmployeeModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{employee_id}", response_model=EmployeeSchema, summary="Получение сотрудника по ID")
async def get_employee(employee_id: int, session: SessionDep) -> EmployeeSchema:
    """Возвращает сотрудника по ID"""
    query = select(EmployeeModel).where(EmployeeModel.id == employee_id)
    result = await session.execute(query)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.get("/telegram/{id_telegram}", response_model=EmployeeSchema, summary="Получение сотрудника по Telegram ID")
async def get_employee_by_telegram_id(id_telegram: int, session: SessionDep) -> EmployeeSchema:
    """Возвращает сотрудника по Telegram ID"""
    query = select(EmployeeModel).where(EmployeeModel.id_telegram == id_telegram)
    result = await session.execute(query)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.patch("/{employee_id}", summary="Обновление сотрудника по ID")
async def update_employee(employee_id: int, employee_update: EmployeeUpdateSchema, session: SessionDep):
    """Обновляет данные сотрудника по ID"""
    query = select(EmployeeModel).where(EmployeeModel.id == employee_id)
    result = await session.execute(query)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    session.add(employee)
    await session.commit()
    return {"status": "success", "message": "Employee updated"}


@router.patch("/telegram/{id_telegram}", summary="Обновление сотрудника по Telegram ID")
async def update_employee_by_telegram_id(id_telegram: int, employee_update: EmployeeUpdateSchema, session: SessionDep):
    """Обновляет данные сотрудника по Telegram ID"""
    query = select(EmployeeModel).where(EmployeeModel.id_telegram == id_telegram)
    result = await session.execute(query)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    session.add(employee)
    await session.commit()
    return {"status": "success", "message": "Employee updated"}


@router.delete("/{employee_id}", summary="Удаление сотрудника по ID")
async def delete_employee(employee_id: int, session: SessionDep):
    """Удаляет сотрудника из БД по ID"""
    query = select(EmployeeModel).where(EmployeeModel.id == employee_id)
    result = await session.execute(query)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await session.delete(employee)
    await session.commit()
    return {"status": "success", "message": "Employee deleted"}


@router.delete("/telegram/{id_telegram}", summary="Удаление сотрудника по Telegram ID")
async def delete_employee_by_telegram_id(id_telegram: int, session: SessionDep):
    """Удаляет сотрудника из БД по Telegram ID"""
    query = select(EmployeeModel).where(EmployeeModel.id_telegram == id_telegram)
    result = await session.execute(query)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await session.delete(employee)
    await session.commit()
    return {"status": "success", "message": "Employee deleted"}