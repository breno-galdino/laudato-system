from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WarningBase(BaseModel):
    title: str
    event_date: datetime 
    content: str
    category_id: int
    
class WarningCreate(WarningBase):
    pass

class WarningUpdate(BaseModel):
    title: Optional[str] = None
    event_date: Optional[datetime] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

class WarningRead(WarningBase):
    id: int