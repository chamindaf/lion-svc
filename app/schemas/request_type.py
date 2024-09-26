from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequestTypeBase(BaseModel):
    """
    Base model for user-related data. 
    This serves as a common schema for user data across various endpoints.
    """
    request_type_id: Optional[int] | None
    outlet_type: str
    request_type: str

class RequestTypeRead(RequestTypeBase):
    """
    Model for reading user data from the database. Includes timestamps.
    """