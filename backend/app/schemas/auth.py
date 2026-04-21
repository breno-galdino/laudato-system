from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str
    parish_slug: str

class UserResponse(UserBase):
    id: UUID
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime
    scopes: list[str] = []

    model_config = SettingsConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username:  Optional[str] = None
    email:     Optional[EmailStr] = None


class UserSimple(BaseModel):
    id: UUID
    username: str
    full_name: Optional[str] = None
    email: str
    is_active: bool
    scopes: list[str] = []
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: UUID | None = None
    parish_id: UUID | None = None
    scopes: list[str] = []


class LoginResponse(BaseModel):
    message: str
    parish_id: UUID
    parish_slug: str
    parish_name: str
