from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class CelebrationCreate(BaseModel):
    date: datetime
    description: Optional[str] = None


class CelebrationRead(BaseModel):
    id: int
    date: datetime
    description: Optional[str] = None


class CelebrationUpdate(BaseModel):
    date: Optional[datetime] = None
    description: Optional[str] = None


class RoleRead(BaseModel):
    id: int
    name: str


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: Optional[str] = None


class AssignmentUpdate(BaseModel):
    celebration_id: Optional[int] = None
    user_id: Optional[UUID] = None
    role_id: Optional[int] = None


class AssignmentRead(BaseModel):
    id: int
    celebration_id: int
    user_id: UUID
    role_id: int


class AssignmentRole(BaseModel):
    user_id: UUID
    role_id: int


class AssignmentDetail(BaseModel):
    id: int
    user_id: UUID
    user_name: str
    role_id: int
    role_name: str


class CelebrationReadFull(BaseModel):
    id: int
    date: datetime
    description: Optional[str] = None
    assignments: list[AssignmentDetail] = []
