from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOOKS_SERVICE_URL: str
    AUTH_SERVICE_URL: str
    REDIS_URL: str
    DEBUG: bool = False 

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"  
        extra = "ignore"

settings = Settings()