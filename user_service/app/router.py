from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.database as db
from app.database import get_db
from app.models import Book, User
from app.schemas import BookCreate

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("")
async def get_user(db: AsyncSession = Depends(get_db)):
    """Получение информации о пользователе по ID"""
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return {'users': users}