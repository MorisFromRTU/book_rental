from fastapi import APIRouter, HTTPException
import httpx
from pydantic_settings import BaseSettings
from starlette.responses import JSONResponse


class Settings(BaseSettings):
    user_service_url: str = "http://user-service:8000"

settings = Settings()
users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/", tags=["Users"])
async def get_users():
    """Получение всех пользователей"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.user_service_url}/users")
            response.raise_for_status() 
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обращении к user-service: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@users_router.post("/register", tags=["Users"])
async def register_user(user_data: dict):
    """Регистрация пользователя"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{settings.user_service_url}/users/register", json=user_data)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обращении к user-service: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)