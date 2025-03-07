from app.services.book_service import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_db 

def get_books_service(db: AsyncSession = Depends(get_db)) -> BookService:
    """Фабрика для создания BooksSerive"""
    return BookService(db)