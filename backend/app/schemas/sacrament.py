from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing import Optional
from datetime import datetime, date
from uuid import UUID

SACRAMENT_TYPES = (
    "batismo",
    "eucaristia",
    "crisma",
    "matrimonio",
    "ordenacao",
    "uncao",
    "penitencia",
)


class SacramentBase(BaseModel):
    sacrament_type: str
    person_name: str
    person_dob: Optional[date] = None
    sacrament_date: date
    officiant: Optional[str] = None
    godfather: Optional[str] = None
    godmother: Optional[str] = None
    witness1: Optional[str] = None
    witness2: Optional[str] = None
    certificate_number: Optional[str] = None
    observations: Optional[str] = None


class SacramentCreate(SacramentBase):
    pass


class SacramentUpdate(BaseModel):
    sacrament_type: Optional[str] = None
    person_name: Optional[str] = None
    person_dob: Optional[date] = None
    sacrament_date: Optional[date] = None
    officiant: Optional[str] = None
    godfather: Optional[str] = None
    godmother: Optional[str] = None
    witness1: Optional[str] = None
    witness2: Optional[str] = None
    certificate_number: Optional[str] = None
    observations: Optional[str] = None


class SacramentRead(SacramentBase):
    id: int
    parish_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)
