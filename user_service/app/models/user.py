from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, func, Index, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
