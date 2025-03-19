from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import jwt
import os

class AuthService:
    def __init__(self):
        load_dotenv()
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = "HS256"
    
    async def create_access_token(self, data, expires_delta: timedelta = timedelta(minutes=15)):
        """Генерация токена доступа"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_access_token(self, headers: dict) -> dict:
        try:
            token = headers.get('Authorization')
            print('token is: ', token.split()[1])
            payload = jwt.decode(token.split()[1], self.SECRET_KEY, algorithms=[self.ALGORITHM])
            print(payload)
            return payload
        except jwt.PyJWTError:
            return None
        

    