from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Diocese(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    state: str = Field(max_length=2)  # UF ex: SP, RJ, MG
    created_at: datetime = Field(default_factory=datetime.utcnow)
