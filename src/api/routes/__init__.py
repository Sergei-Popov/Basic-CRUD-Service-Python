from .admin import router as admin_router
from .users import router as users_router
from .employees import router as employees_router

__all__ = [
    "admin_router",
    "users_router",
    "employees_router",
]