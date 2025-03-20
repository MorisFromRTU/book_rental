import httpx
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.rental_repository import RentalRepository
from app.config import settings
from fastapi import HTTPException
from app.services.auth_service import auth_service
logger = logging.getLogger(__name__)


class RentalService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = RentalRepository(db_session)
        self.books_service_url = settings.BOOKS_SERVICE_URL

    async def get_available_books(self):
        try:
            async with httpx.AsyncClient() as client:
                logger.info("Получение всех книг из сервиса books")
                response = await client.get(f'{self.books_service_url}/books')
                response.raise_for_status()
                books = response.json()

            logger.info("Получение всех недоступных книг из БД")
            unavailable_books = await self.repository.get_unavailable_books()

            available_books = [
                book for book in books
                if book["id"] not in {ub.book_id for ub in unavailable_books}
            ]

            return {'available_books': available_books}

        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при получении данных из сервиса books: {e}")
            raise HTTPException(
                status_code=400,
                detail="Не удалось получить список книг из сервиса books"
            )
        except Exception as e:
            logger.error(
                f"Неизвестная ошибка в методе in get_available_books: {e}")
            raise Exception("Ошибка получения данных")

    async def get_book_data(self, book_id: int):
        """
        Получение информации о книге
        """
        try:
            async with httpx.AsyncClient() as client:
                logger.info("Получение данных о книге из сервиса books")
                response = await client.get(f'{self.books_service_url}/books/{book_id}')
                response.raise_for_status()
                book = response.json()

                if not book:
                    raise HTTPException(
                        status_code=400,
                        detail="Не удалось получить данные об этой книге из сервиса books"
                    )

            return book

        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при получении данных из сервиса books: {e}")
            raise Exception("Не удалось получить список книг из сервиса books")
        except Exception as e:
            logger.error(
                f"Неизвестная ошибка в методе in get_available_books: {e}")
            raise Exception("Ошибка получения данных")

    async def rent_book(self, headers: dict, book_id: int):
        """
        Бизнес-логика аренды книги
        """
        book = await self.get_book_data(book_id=book_id)
        unavailable_books = await self.repository.get_unavailable_books()
        unavailable_books = [book.book_id for book in unavailable_books]
        book_id = book['book_data']['id']
        if book_id in unavailable_books:
            raise HTTPException(
                status_code=400,
                detail="Данная книга недоступна для аренды"
            )

        user_id = await auth_service.get_current_user(headers=headers)

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Произошла ошибка при получении данных"
            )

        rented_book_id = await self.repository.rent_book(user_id=user_id, book_id=book_id)
        return {'message': 'Книга была успешно взята в аренду', 'rented_book_id': rented_book_id}

    async def return_book(self, headers: dict, book_id: int):
        """
        Бизнес-логика для возврата книги
        """
        user_id = await auth_service.get_current_user(headers=headers)
        unavailable_books = await self.repository.get_unavailable_books()
        unavailable_books = [book.book_id for book in unavailable_books]

        if book_id not in unavailable_books:
            raise HTTPException(
                status_code=400,
                detail="Данная книга недоступна для возврата"
            )

        book_data = await self.repository.get_rental_book_data(
            book_id=book_id,
            user_id=user_id
        )

        if not book_data:
            raise HTTPException(
                status_code=400,
                detail="Данная книга недоступна для возврата"
            )

        if await self.repository.return_book(book_id=book_data.book_id, user_id=user_id) < 1:
            raise HTTPException(
                status_code=400,
                detail="Произошла ошибка при возврате книги"
            )

        return {'message': 'Возврат книги успешно оформлен'}
