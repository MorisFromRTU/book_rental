from fastapi import APIRouter, Request
from app.routers.utils import make_request
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    books_service_url: str = "http://books-service:8000"

settings = Settings()
books_router = APIRouter(prefix="/books", tags=["Books"])

@books_router.get("/")
async def get_books(request: Request):
    """Получение всех книг"""
    return await make_request(
        method="GET",
        url=f"{settings.books_service_url}/books",
        headers=request.headers
    )

@books_router.post("/")
async def create_book(request: Request, book_data: dict):
    """Создание книги"""
    return await make_request(
        method="POST",
        url=f"{settings.books_service_url}/books",
        headers=request.headers,
        json=book_data
    )

@books_router.put("/{book_id}")
async def update_book(request: Request, book_id: int, book_data: dict):
    """Обновление книги"""
    return await make_request(
        method="PUT",
        url=f"{settings.books_service_url}/books/{book_id}",
        headers=request.headers,
        json=book_data
    )

@books_router.get("/{book_id}")
async def get_book_by_id(request: Request, book_id: int):
    """Получение полной информации о книге"""
    return await make_request(
        method="GET",
        url=f"{settings.books_service_url}/books/{book_id}",
        headers=request.headers
    )