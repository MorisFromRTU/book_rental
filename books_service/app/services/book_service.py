from app.repositories.book_repository import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book 

class BookService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = BookRepository(db_session)
    
    async def get_all_books(self) -> list[Book]:
        """Бизнес-логика получения всех книг"""
        return await self.repository.get_all_books()