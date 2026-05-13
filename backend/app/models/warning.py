from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class Warning(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parish_id: Optional[UUID] = Field(default=None, foreign_key="parish.id", index=True)
    title: str = Field(max_length=100)
    event_date: datetime
    content: str = Field(max_length=500)
    category_id: int
    community_id: Optional[int] = Field(default=None, foreign_key="community.id", index=True)