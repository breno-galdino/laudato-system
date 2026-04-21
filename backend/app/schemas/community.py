from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class CommunityCreate(BaseModel):
    name: str
    type: str = "grupo"
    description: Optional[str] = None
    address: Optional[str] = None
    coordinator: Optional[str] = None
    meeting_day: Optional[str] = None
    meeting_time: Optional[str] = None


class CommunityRead(BaseModel):
    id: int
    parish_id: UUID
    name: str
    type: str
    description: Optional[str] = None
    address: Optional[str] = None
    coordinator: Optional[str] = None
    meeting_day: Optional[str] = None
    meeting_time: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class CommunityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    coordinator: Optional[str] = None
    meeting_day: Optional[str] = None
    meeting_time: Optional[str] = None
    is_active: Optional[bool] = None
