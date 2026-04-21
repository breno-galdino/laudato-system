from graphemy import Graphemy, Field, Dl
from datetime import datetime
from uuid import UUID

class Celebration(Graphemy, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parish_id: UUID | None = Field(default=None, foreign_key="parish.id", index=True)
    date: datetime
    description: str | None = None


class Role(Graphemy, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parish_id: UUID | None = Field(default=None, foreign_key="parish.id", index=True)
    name: str

class Assignment(Graphemy, table=True):
    id: int | None = Field(default=None, primary_key=True)
    celebration_id: int = Field(foreign_key="celebration.id")
    user_id: UUID = Field(foreign_key="user.id")
    role_id: int = Field(foreign_key="role.id")
    
    celebration: "Celebration" = Dl(source="celebration_id", target="id")
    user: "User" = Dl(source="user_id", target="id")
    role: "Role" = Dl(source="role_id", target="id")
    
    