from fastapi import FastAPI
from .routers.rental_router import rental_router

app = FastAPI()

app.include_router(rental_router)