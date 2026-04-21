from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing import Optional


class DioceseRead(BaseModel):
    id: int
    name: str
    state: str

    model_config = SettingsConfigDict(from_attributes=True)


class DioceseCreate(BaseModel):
    name: str
    state: str


class DioceseUpdate(BaseModel):
    name: Optional[str] = None
    state: Optional[str] = None
