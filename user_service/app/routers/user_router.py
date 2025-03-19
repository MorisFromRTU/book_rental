from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database import get_db
from functools import wraps
from app.services.user_service import UserService
from app.schemas import UserCreate, UserLogin
from app.routers.utils import get_user_service

def handle_value_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return wrapper

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("")
@handle_value_errors
async def get_users(service: UserService = Depends(get_user_service) , db: AsyncSession = Depends(get_db)):
    """Получение всех пользователей"""
    users = await service.get_all_users()
    return users

@users_router.post("/register")
@handle_value_errors
async def register_user(
    request: Request,
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """Регистрация пользователя"""
    user = await service.create_user(user_data)
    return user
    
@users_router.post("/login")
@handle_value_errors
async def user_login(
    request: Request,
    user_data: UserLogin, 
    service: UserService = Depends(get_user_service), 
    db: AsyncSession = Depends(get_db)
):
    """Логин пользователя"""
    token = await service.user_login(user_data=user_data, db=db)
    return token
