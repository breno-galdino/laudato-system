from graphemy import Dl, Field, Graphemy
from typing import Optional


class Category(Graphemy, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, index=True)
    description: str = Field(max_length=200)
    icon: str = Field(max_length=30)