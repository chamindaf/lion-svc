from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReqBrandingElementsTypeBase(BaseModel):
    """
    Base model for request branding elements type data.
    Serves as a common schema for shared fields across endpoints.
    """
    req_branding_elements_type_id: Optional[int] = None
    request_type_id: Optional[int] = None
    request_type: Optional[str] = None
    branding_elements_type_id: Optional[int] = None
    branding_elements_type: Optional[str] = None
    is_active: Optional[bool] = None

class ReqBrandingElementsTypeRead(ReqBrandingElementsTypeBase):
    """
    Schema for reading request branding elements type data from the database.
    Includes timestamps and metadata.
    """
    req_branding_elements_type_id: int
    request_type_id: int
    request_type: str
    branding_elements_type_id: int
    branding_elements_type: str
    is_active: bool
    created_on: Optional[datetime] = None
    created_by: str
    updated_on: Optional[datetime] = None
    updated_by: Optional[str] = None

    class ConfigDict:
        """
        Pydantic configuration to enable loading attributes 
        from ORM-style models.
        """
        from_attributes = True

class ReqBrandingElementsTypeCreate(BaseModel):
    """
    Schema for creating a new request branding elements type.
    Requires the necessary fields for creation.
    """
    request_type_id: Optional[int] = None
    request_type: str
    outlet_type: Optional[str] = None
    branding_elements_type_id: Optional[int] = None
    branding_elements_type: str

class ReqBrandingElementsTypeUpdate(BaseModel):
    """
    Schema for updating existing request branding elements type information.
    Includes all fields required for updates.
    """
    req_branding_elements_type_id: int
    is_active: bool