from sqlalchemy.ext.asyncio import AsyncSession
import app.database as db
from fastapi import APIRouter, Depends
from app.database import get_db
import app.services as service

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("")
async def get_user(db: AsyncSession = Depends(get_db)):
    """Получение информации о пользователе по ID"""
    users = await service.get_all_users(db=db)
    return {'users': users}