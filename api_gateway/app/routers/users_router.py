from fastapi import APIRouter, Request
from app.routers.utils import make_request
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user_service_url: str = "http://user-service:8000"

settings = Settings()
users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/")
async def get_users(request: Request):
    """Получение всех пользователей"""
    return await make_request(
        method="GET",
        url=f"{settings.user_service_url}/users",
        headers=request.headers
    )

@users_router.post("/register")
async def register_user(request: Request, user_data: dict):
    """Регистрация пользователя"""
    return await make_request(
        method="POST",
        url=f"{settings.user_service_url}/users/register",
        headers=request.headers,
        json=user_data
    )

@users_router.post("/login")
async def user_login(request: Request, user_data: dict):
    """Логин пользователя"""
    return await make_request(
        method="POST",
        url=f"{settings.user_service_url}/users/login",
        headers=request.headers,
        json=user_data
    )
