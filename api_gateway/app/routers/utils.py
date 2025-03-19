import httpx
from fastapi import HTTPException

async def make_request(method: str, headers: dict, url: str, json: dict = None):
    """Общая функция для выполнения HTTP-запросов"""
    filtered_headers = {
            "Content-Type": "application/json",
        }
    if headers.get("authorization"):
        filtered_headers["Authorization"] = headers["authorization"]
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url=url, headers=filtered_headers)
            elif method == "POST":
                response = await client.post(url=url, json=json, headers=filtered_headers)
            elif method == "PUT":
                response = await client.put(url=url, json=json, headers=filtered_headers)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обращении к service: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)