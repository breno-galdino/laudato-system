from graphemy import Graphemy, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID


class Community(Graphemy, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parish_id: UUID = Field(foreign_key="parish.id", index=True)
    name: str = Field(max_length=100)
    type: str = Field(default="grupo", max_length=20)   # "grupo" | "pastoral"
    description: Optional[str] = Field(default=None, max_length=500)
    address: Optional[str] = Field(default=None, max_length=200)
    coordinator: Optional[str] = Field(default=None, max_length=100)
    meeting_day: Optional[str] = Field(default=None, max_length=20)
    meeting_time: Optional[str] = Field(default=None, max_length=10)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
