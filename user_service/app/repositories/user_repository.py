from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from app.schemas import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self) -> list[User]:
        """Получение всех пользователей из базы данных"""
        query = select(User)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Получение пользователя по ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Получение пользователя по username"""
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Получение пользователя по username"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate, hashed_password: str):
        """Создание нового пользователя"""
        new_user = User(
            username=user_data.username,
            name=user_data.name,
            surname=user_data.surname,
            password=hashed_password,
            email=user_data.email
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user.id
