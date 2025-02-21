from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.database as db
from app.models import Book
from app.schemas import BookCreate

books_router = APIRouter()

@books_router.get('/')
async def users(db: AsyncSession = Depends(db.get_db)):
    query = select(Book)
    result = await db.execute(query)
    books = result.scalars().all()
    return {'books': books}

@books_router.post('/')
async def users(book_data: BookCreate, db: AsyncSession = Depends(db.get_db)):
    book = Book(
        title=book_data.title,
        author=book_data.author,
        price=book_data.price
    )
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return {'message': f'Была создана новая книга {book.title}'}