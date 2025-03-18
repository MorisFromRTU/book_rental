"""
Роутер для работы с книгами
"""
from fastapi import APIRouter, Depends, HTTPException, status
from functools import wraps
from app.routers.utils import get_books_service
from app.services.book_service import BookService
from app.schemas.book import BookCreate, BookUpdate


def handle_value_errors(func):
    """
    Обработчик ошибок при запросах
    """
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
async def get_books(
    service: BookService = Depends(get_books_service)
):
    """Получение информации о всех книгах"""
    books = await service.get_all_books()
    return books


@books_router.post("", status_code=201)
@handle_value_errors
async def create_book(
    book_data: BookCreate,
    service: BookService = Depends(get_books_service)
):
    """Создание записи о новой книги"""
    book_id = await service.create_book(book_data=book_data)
    return {'book_id': book_id}


@books_router.put("/{book_id}", status_code=200)
@handle_value_errors
async def update_book(book_id: int, book_data: BookUpdate, service: BookService = Depends(get_books_service)):
    """Обновление записи о существующей книге"""
    updated_book = await service.update_book(book_id=book_id, book_data=book_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {'book_data': updated_book}

@books_router.get("/{book_id}", status_code=200)
@handle_value_errors
async def get_book_by_id(book_id: int, service: BookService = Depends(get_books_service)):
    """Получение записи о существующей книге"""
    book = await service.get_book(book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {'book_data': book}
