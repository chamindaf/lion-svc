from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class LookupBase(BaseModel):
    category: Optional[str] = None
    display_value: Optional[str] = None
    sort: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[str] = None
    created_on: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_on: Optional[datetime] = None

class LookupRead(LookupBase):
    lookup_id: int
    pass