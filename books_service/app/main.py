from fastapi import FastAPI
from app.routers.book_router import books_router

app = FastAPI()

app.include_router(books_router)