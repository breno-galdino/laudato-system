from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: str
    icon: str

class CategoryRead(CategoryCreate):
    id: int

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None