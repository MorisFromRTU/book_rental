import httpx
from typing import Literal
from fastapi import HTTPException

async def make_request(method: Literal["GET", "POST"], url: str, json: dict = None):
    """Общая функция для выполнения HTTP-запросов"""
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=json)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обращении к user-service: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)