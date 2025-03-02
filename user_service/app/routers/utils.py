from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_db 

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Фабрика для создания UserService"""
    return UserService(db)