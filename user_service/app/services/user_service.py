from app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
from passlib.context import CryptContext
from app.models.user import User
from app.schemas import UserCreate, UserLogin
from fastapi import HTTPException, status
import bcrypt
import httpx


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = UserRepository(db_session)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.auth_service_url: str = "http://auth-service:8000"

    async def get_all_users(self) -> list[User]:
        """Бизнес-логика получения всех пользователей"""
        return await self.repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Бизнес-логика получения пользователя по ID"""
        return await self.repository.get_user_by_id(user_id)

    async def verify_password(
            self,
            plain_password: str,
            hashed_password: str) -> bool:
        """Проверка корректности пароля"""
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(
            self,
            db: AsyncSession,
            username: str,
            password: str) -> User:
        user = await self.repository.get_user_by_username(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not await self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect password"
            )
        return user

    async def create_user(self, user_data: UserCreate):
        """Бизнес-логика регистрации пользователя"""
        if await self.repository.get_user_by_username(
            username=user_data.username
        ):
            raise ValueError(
                "Пользователь с таким именем ником уже сущетсвует"
            )

        if await self.repository.get_user_by_email(
            email=user_data.email
        ):
            raise ValueError(
                "Пользователь с такой почтой уже сущетсвует"
            )

        hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"),
                                        bcrypt.gensalt()).decode("utf-8")

        if not hashed_password:
            raise ValueError('Ошибка при создании пользователя')

        user_id = await self.repository.create_user(
            user_data=user_data,
            hashed_password=hashed_password
            )
        
        return {"message": "User created successfully", "user_id": user_id}

    async def user_login(self, user_data: UserLogin, db: AsyncSession):
        """Бизнес-логика логина пользователя"""
        user = await self.authenticate_user(
            username=user_data.username,
            password=user_data.password,
            db=db
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect password"
            )
        user_data: dict = {"user_id": user.id}
        async with httpx.AsyncClient() as client:
            try:
                token = await client.post(
                    f"{self.auth_service_url}/auth/token",
                    json=user_data
                )
                token.raise_for_status()
                return token.json()
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Ошибка при обращении к user-service: {e}"
                )
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=e.response.text
                )
