import httpx
import logging
from app.config import settings
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

logger = logging.getLogger(__name__)

class AuthSerivice:
    def __init__(self):
        self.AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL

    async def get_current_user(self, headers: dict):
        """
        Получает user_id из сервиса users.
        """
        try:
            token = headers.get('authorization')
            if not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid token format")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.AUTH_SERVICE_URL}/auth/verify_token",
                    headers={"Authorization": f"{token}"}
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=401, detail="Invalid token")
                data = response.json()
                if not data.get('user_id'):
                    raise HTTPException(status_code=401, detail="Invalid token")
                return data["user_id"]
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка при получении данных из сервиса auth: {e}")
            raise Exception("Не удалось подтвердить токен в сервисе auth")
        
auth_service = AuthSerivice()