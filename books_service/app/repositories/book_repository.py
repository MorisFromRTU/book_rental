from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.exc import SQLAlchemyError


class BookRepository:
    """
    Репозиторий для работы с книгами в базе данных.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self) -> list[Book]:
        """
        Получение всех книг из базы данных.
        """
        query = select(Book)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_book_by_id(self, book_id: int) -> Book:
        """
        Получение книги по ID.
        """
        query = select(Book).where(Book.id == book_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def add_book(self, book_data: BookCreate) -> int:
        """
        Создание записи о книге в базе данных.
        Возвращает ID созданной книги.
        """
        try:
            query = (
                insert(Book)
                .values(
                    title=book_data.title,
                    author=book_data.author,
                    price=book_data.price,
                )
            )
            result = await self.db.execute(statement=query)
            await self.db.commit()
            book_id = result.inserted_primary_key[0]
            return book_id
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")

    async def update_book(self,
                          book_id: int,
                          book_data: BookUpdate
                          ) -> None:
        """
        Обновление записи о книге в базе данных.
        Функция ничего не возвращает.
        """
        try:
            query = (
                update(Book)
                .where(Book.id == book_id)
                .values(
                    title=book_data.title,
                    author=book_data.author,
                    price=book_data.price,
                )
            )
            await self.db.execute(statement=query)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")
