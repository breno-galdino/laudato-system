from graphemy import Dl, Field, Graphemy
from typing import Optional
from uuid import UUID


class Category(Graphemy, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parish_id: Optional[UUID] = Field(default=None, foreign_key="parish.id", index=True)
    name: str = Field(max_length=50, index=True)
    description: str = Field(max_length=200)
    icon: str = Field(max_length=30)