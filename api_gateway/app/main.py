from fastapi import FastAPI, HTTPException
import httpx 
from pydantic_settings import BaseSettings
from starlette.responses import JSONResponse

# Настройка переменных окружения
class Settings(BaseSettings):
    user_service_url: str = "http://user-service:8000" 
    book_service_url: str = "http://book-service:8000"  
    rental_service_url: str = "http://rental-service:8000"  

settings = Settings()

app = FastAPI(title="API Gateway", description="Обработка запросов между микросервисами")

@app.get("/users", tags=["Users"])
async def get_users():
    """Получение всех пользователей"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.user_service_url}/users")
            response.raise_for_status() 
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обращении к user-service {e}")

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Проверка доступности API Gateway"""
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.get("/", tags=["Root"])
async def root():
    """Корневой эндпоинт API Gateway"""
    return {"message": "Добро пожаловать на сервис аренды книг"}