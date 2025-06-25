from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    is_active: Optional[bool] = True
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserCreate(User):
    email: EmailStr
    password: str
    username: str

class UserResponse(User):
    id: int
    full_name: Optional[str] = None
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
