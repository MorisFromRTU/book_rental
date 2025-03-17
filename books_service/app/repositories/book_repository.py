from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book
from app.schemas.book import BookCreate
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self) -> list[Book]:
        """Получение всех книг из базы данных"""
        query = select(Book)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def add_book(self, book_data: BookCreate) -> int:
        """
        Создание записи о книге в базе данных.
        Возвращает ID созданной книги.
        """
        try:
            query = insert(Book).values(
                title=book_data.title,
                author=book_data.author,
                price=book_data.price
            )
            result = await self.db.execute(statement=query)
            await self.db.commit()
            book_id = result.inserted_primary_key[0]
            return book_id
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")