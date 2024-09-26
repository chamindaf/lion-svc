from pydantic import BaseModel
from typing import Optional

class BrandingElementsTypeBase(BaseModel):
    """
    Base model for user-related data. 
    This serves as a common schema for user data across various endpoints.
    """
    branding_elements_type_id: Optional[int] | None
    branding_elements_type: str

class BrandingElementsTypeRead(BrandingElementsTypeBase):
    """
    Model for reading user data from the database. Includes timestamps.
    """