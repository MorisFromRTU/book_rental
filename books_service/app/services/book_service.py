from app.repositories.book_repository import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book 
from app.schemas.book import BookCreate

class BookService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = BookRepository(db_session)
    
    async def get_all_books(self) -> list[Book]:
        """Бизнес-логика получения всех книг"""
        return await self.repository.get_all_books()
    
    async def create_book(self, book_data: BookCreate) -> int:
        """Бизнес-логика для создания записи о книге"""
        return await self.repository.add_book(book_data)