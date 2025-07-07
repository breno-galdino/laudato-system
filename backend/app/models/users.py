from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class UserScope(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    scope_id: int = Field(foreign_key="scope.id", primary_key=True)

class Scope(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    
    users: List["User"] = Relationship(back_populates="scopes", link_model=UserScope)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    email: str = Field(max_length=150, unique=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    scopes: List[Scope] = Relationship(back_populates="users", link_model=UserScope)
    
    @property
    def is_admin(self) -> bool:
        return any(scope.name == "admin" for scope in self.scopes)
