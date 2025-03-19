from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends 
from database import get_db
from app.services.rental_service import RentalService

def get_rental_service(db: AsyncSession = Depends(get_db)) -> RentalService:
    """Фабрика для создания RentalService"""
    return RentalService(db_session=db)