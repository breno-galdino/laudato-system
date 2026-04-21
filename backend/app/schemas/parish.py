from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class ParishCreate(BaseModel):
    name: str
    slug: str
    diocese_id: Optional[int] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ParishRead(BaseModel):
    id: UUID
    name: str
    slug: str
    diocese_id: Optional[int] = None
    diocese_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None
    whatsapp: Optional[str] = None
    plan: str
    is_active: bool
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class ParishUpdate(BaseModel):
    name: Optional[str] = None
    diocese_id: Optional[int] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None
    whatsapp: Optional[str] = None


class ParishRegister(BaseModel):
    """Cria uma paróquia junto com seu primeiro usuário admin."""
    parish: ParishCreate
    admin_full_name: str
    admin_email: EmailStr
    admin_username: str
    admin_password: str
