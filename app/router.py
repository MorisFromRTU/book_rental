from .routes.books import books_router
from fastapi import FastAPI

def setup_routes(app: FastAPI):
    app.include_router(books_router, prefix="/books")