from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str | None = Field(max_length=100)
    email: str = Field(max_length=150, unique=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Scope(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

class UserScope(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    scope_id: int = Field(foreign_key="scope.id", primary_key=True)
