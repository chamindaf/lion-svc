from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandingElementBase(BaseModel):
    """
    Base model for user-related data. 
    This serves as a common schema for user data across various endpoints.
    """
    req_branding_elements_type_id: Optional[int] = None
    request_id: int
    branding_element: str
    created_on: datetime
    created_by: str

class BrandingElementRead(BrandingElementBase):
    """
    Model for reading user data from the database. Includes timestamps.
    """
    branding_element_id: int
    req_branding_elements_type: str
    request_id: int
    branding_element: str
    created_on: datetime
    created_by: str

    class Config:
        """
        Pydantic configuration to enable loading attributes 
        from ORM-style models.
        """
        from_attributes = True

class BrandingElementCreate(BaseModel):
    req_branding_elements_type_id: int
    request_id: int
    branding_element: str
    created_by: Optional[str] = None