"""
Сущность Аренды
"""
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()


class RentalBook(Base):
    """
    Модель для описания таблица аренды
    """
    __tablename__ = "rental_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    rented_at = Column(DateTime, default=datetime.now())
    returned_at = Column(DateTime, nullable=True)
