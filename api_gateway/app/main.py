from fastapi import FastAPI
from pydantic_settings import BaseSettings
from starlette.responses import JSONResponse
from app.routers import users_router, books_router, rental_router
# Настройка переменных окружения
class Settings(BaseSettings):
    user_service_url: str = "http://user-service:8000" 
    auth_service_url: str = "http://auth-service:8000"  
    books_service_url: str = "http://books-service:8000"
    rental_service_url: str = "http://rental-service:8000"

settings = Settings()

app = FastAPI(title="API Gateway", description="Обработка запросов между микросервисами")

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Проверка доступности API Gateway"""
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.get("/", tags=["Root"])
async def root():
    """Корневой эндпоинт API Gateway"""
    return {"message": "Добро пожаловать на сервис аренды книг"}

app.include_router(router=users_router)
app.include_router(router=books_router)
app.include_router(router=rental_router)