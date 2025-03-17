from fastapi import APIRouter
from app.routers.utils import make_request
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    books_service_url: str = "http://books-service:8000"

settings = Settings()
books_router = APIRouter(prefix="/books", tags=["Books"])

@books_router.get("/")
async def get_books():
    """Получение всех книг"""
    return await make_request("GET", f"{settings.books_service_url}/books")

@books_router.post("/")
async def create_book(book_data: dict):
    """Создание книги"""
    return await make_request("POST", f"{settings.books_service_url}/books", book_data)