from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from functools import wraps
from app.routers.utils import get_books_service
from app.services.book_service import BookService

def handle_value_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return wrapper

books_router = APIRouter(prefix="/books", tags=["Books"])

@books_router.get("")
@handle_value_errors
async def get_books(service: BookService = Depends(get_books_service) , db: AsyncSession = Depends(get_db)):
    """Получение информации о всех книгах"""
    books = await service.get_all_books()
    return books
