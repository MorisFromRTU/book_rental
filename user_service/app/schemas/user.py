from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    price: int = Field(gt=0)

class UserCreate(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr
    password: str
    age: int | None = Field(default=None)

class UserLogin(BaseModel):
    username: str
    password: str