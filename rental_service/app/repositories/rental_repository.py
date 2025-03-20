from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.rental import RentalBook
from datetime import datetime


class RentalRepository:
    """
    Репозиторий для работы с арендами в базе данных.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_unavailable_books(self) -> list[RentalBook]:
        """
        Получение недоступных книг из базы данных.
        """
        query = (
            select(RentalBook)
            .where(RentalBook.rented_at.is_not(None))
            .where(RentalBook.returned_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def rent_book(self, user_id: int, book_id: int) -> int:
        """
        Создание в базе данных записи об аренде книги
        """
        rented_book = RentalBook(
            user_id=user_id,
            book_id=book_id
        )

        self.db.add(rented_book)
        await self.db.commit()
        await self.db.refresh(rented_book)
        return rented_book.id

    async def get_rental_book_data(self, book_id: int, user_id: int) -> RentalBook:
        """
        Получить информацию об арендованной книге
        """
        query = (
            select(RentalBook)
            .where(
                RentalBook.book_id == book_id,
                RentalBook.user_id == user_id,
                RentalBook.rented_at.is_not(None),
                RentalBook.returned_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def return_book(self, book_id: int, user_id: int):
        query = (
            update(RentalBook)
            .where(
                RentalBook.book_id == book_id,
                RentalBook.user_id == user_id,
                RentalBook.rented_at.is_not(None),
                RentalBook.returned_at.is_(None)
            )
            .values(
                returned_at=datetime.now()
            )
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount
