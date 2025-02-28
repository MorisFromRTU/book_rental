from sqlalchemy.ext.asyncio import AsyncSession
import app.database as db
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
import app.services as service
from app.services.user_service import UserService
from app.schemas import UserCreate

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("")
async def get_user(db: AsyncSession = Depends(get_db)):
    """Получение информации о пользователе по ID"""
    service = UserService(db)
    try:
        user = await service.get_all_users()
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@users_router.post("/register")
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрация пользователя"""
    service = UserService(db)
    try:
        user = await service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))