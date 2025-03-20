from fastapi import APIRouter, Request
from app.routers.utils import make_request
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Настройки роутера для взаимодействия с сервисом аренды
    """
    rental_service_url: str = "http://rental-service:8000"

settings = Settings()
rental_router = APIRouter(prefix="/rental", tags=["Rental"])

@rental_router.get("/books")
async def get_avaliable_books(request: Request):
    """Получение всех доступных для аренды книг"""
    return await make_request(
        method="GET",
        url=f"{settings.rental_service_url}/rental/books",
        headers=request.headers
    )

@rental_router.post("/books/{book_id}")
async def rent_book(request: Request, book_id: int):
    """Аренда книги"""
    return await make_request(
        method="POST",
        url=f"{settings.rental_service_url}/rental/books/{book_id}",
        headers=request.headers,
        json=await request.json()
    )

@rental_router.put("/books/{book_id}/return")
async def return_book(request: Request, book_id: int):
    """Возврат книги"""
    return await make_request(
        method="PUT",
        url=f"{settings.rental_service_url}/rental/books/{book_id}/return",
        headers=request.headers,
        json=await request.json()
    )
