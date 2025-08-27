from sqlmodel import Relationship
from graphemy import Dl, Field, Graphemy
from typing import Optional, List
from datetime import datetime, timezone
from uuid import uuid4, UUID

class UserScope(Graphemy, table=True):
    __tablename__ = "user_scope"
    __queryname__ = "user_scope"
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    scope_id: int = Field(foreign_key="scope.id", primary_key=True)
    
    user: list["User"] = Dl(source="user_id", target="id")
    # scope: List["Scope"] = Dl(source="scope_id", target="id")

class Scope(Graphemy, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    
    user_scopes: list["UserScope"] = Dl(source="id", target="scope_id")
    
    # users: List["User"] = Relationship(back_populates="scopes", link_model=UserScope)

class User(Graphemy, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    email: str = Field(max_length=150, unique=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    scopes: list["UserScope"] = Dl(source="id", target="user_id")
    
    # scopes: List[Scope] = Relationship(back_populates="users", link_model=UserScope)
    
    @property
    def is_admin(self) -> bool:
        return any(scope.name == "admin" for scope in self.scopes)
