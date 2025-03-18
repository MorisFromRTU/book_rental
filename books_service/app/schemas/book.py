from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    price: int = Field(gt=0)

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    price: Optional[int]
