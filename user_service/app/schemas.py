from pydantic import BaseModel, Field
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    price: int = Field(gt=0)
