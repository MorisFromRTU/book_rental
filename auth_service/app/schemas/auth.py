from pydantic import BaseModel, Field

class TokenCreate(BaseModel):
    user_id: int
