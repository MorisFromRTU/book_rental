from app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas import UserCreate
import bcrypt

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = UserRepository(db_session)
    
    async def get_all_users(self) -> list[User]:
        """Бизнес-логика получения всех пользователей"""
        return await self.repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Бизнес-логика получения пользователя по ID"""
        return await self.repository.get_user_by_id(user_id)

    async def create_user(self, user_data: UserCreate):
        """Бизнес логика регистрации пользователя"""
        print(self.repository.get_user_by_username(username=user_data.username))
        if await self.repository.get_user_by_username(username=user_data.username):
            raise ValueError("Пользователь с таким именем ником уже сущетсвуте")
        
        if await self.repository.get_user_by_email(email=user_data.email):
            raise ValueError("Пользователь с такой почтой уже сущетсвуте")

        hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        if not hashed_password:
            raise ValueError('Ошибка при создании пользователя')
        
        return await self.repository.create_user(user_data=user_data, hashed_password=hashed_password)