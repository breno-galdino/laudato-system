from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str

class UserResponse(UserBase):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
