from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book
from sqlalchemy import select

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self) -> list[Book]:
        """Получение всех книг из базы данных"""
        query = select(Book)
        result = await self.db.execute(query)
        return result.scalars().all()