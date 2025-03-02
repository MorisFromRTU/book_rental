from fastapi import APIRouter
from app.routers.utils import make_request
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user_service_url: str = "http://user-service:8000"

settings = Settings()
users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/")
async def get_users():
    """Получение всех пользователей"""
    return await make_request("GET", f"{settings.user_service_url}/users")

@users_router.post("/register")
async def register_user(user_data: dict):
    """Регистрация пользователя"""
    return await make_request("POST", f"{settings.user_service_url}/users/register", json=user_data)

@users_router.post("/login")
async def user_login(user_data: dict):
    """Логин пользователя"""
    return await make_request("POST", f"{settings.user_service_url}/users/login", json=user_data)
