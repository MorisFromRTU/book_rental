from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models import User
from sqlalchemy import select
async def get_all_users(db: AsyncSession) -> List[User]:
    """
    Получение списка всех пользователей
    """
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return users