from functools import wraps
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.services.auth_service import AuthService
from app.routers.utils import get_auth_service
from app.schemas.auth import TokenCreate


def handle_value_errors(func):
    """Декоратор для обработки HTTP ошибок"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e))
    return wrapper


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/token")
@handle_value_errors
async def create_token(user_data: TokenCreate,
                       service: AuthService = Depends(get_auth_service)):
    """Создание токена доступа"""
    access_token = await service.create_access_token(
        data={"user_id": user_data.user_id},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/verify_token")
@handle_value_errors
async def verify_token(request: Request,
                       service: AuthService = Depends(get_auth_service)):
    """Получение данных о пользователе по токену"""
    return await service.get_access_token(headers=request.headers)
