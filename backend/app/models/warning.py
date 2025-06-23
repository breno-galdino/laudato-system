from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Warning(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    event_date: datetime
    content: str = Field(max_length=500)
    category_id: int