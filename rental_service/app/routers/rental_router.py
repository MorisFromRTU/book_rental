"""
Роутер для работы с арендой
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from functools import wraps
from app.services.rental_service import RentalService
from app.routers.utils import get_rental_service

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

rental_router = APIRouter(prefix="/rental", tags=["Rental"])

@rental_router.get("/books")
@handle_value_errors
async def get_books(
    request: Request,
    service: RentalService = Depends(get_rental_service)
):
    """Получение информации о доступных книгах"""
    return await service.get_available_books()

@rental_router.post("/books/{book_id}")
@handle_value_errors
async def rent_book(
    book_id: int,
    request: Request,
    service: RentalService = Depends(get_rental_service)
):
    """Аренда книги"""
    return await service.rent_book(headers=request.headers, book_id=book_id)

@rental_router.put("/books/{book_id}/return")
@handle_value_errors
async def rent_book(
    book_id: int,
    request: Request,
    service: RentalService = Depends(get_rental_service)
):
    """Возврат книги"""
    return await service.return_book(headers=request.headers, book_id=book_id)