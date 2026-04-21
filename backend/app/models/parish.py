from graphemy import Graphemy, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4, UUID


class Parish(Graphemy, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100)
    slug: str = Field(max_length=50, unique=True, index=True)
    address: Optional[str] = Field(default=None, max_length=200)
    email: Optional[str] = Field(default=None, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)
    is_active: bool = Field(default=True)
    plan: str = Field(default="free", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
