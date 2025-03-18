from fastapi import FastAPI
from .routers.books_router import books_router

app = FastAPI()

app.include_router(books_router)