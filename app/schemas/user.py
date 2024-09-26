from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    Base model for user-related data. 
    This serves as a common schema for user data across various endpoints.
    """
    user_id: Optional[int] = None
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    vendor_id: Optional[int] = None
    company: Optional[str] = None
    contact: Optional[int] = None
    is_active: Optional[bool] = None

class UserUpdate(BaseModel):
    """
    Model for updating user information. Extends from `UserBase`.
    """
    user_id: int
    is_active: bool

class UserCreate(BaseModel):
    """
    Model for creating a new user. Requires `role` in addition to base user data.
    """
    email: EmailStr
    role: str
    first_name: Optional[str]
    last_name: Optional[str]
    vendor_id: int
    company: Optional[str]
    contact: Optional[int]

class UserRead(UserBase):
    """
    Model for reading user data from the database. Includes timestamps.
    """
    email: EmailStr
    role: str
    first_name: str | None
    last_name: str | None
    vendor_id: int
    company: str | None
    contact: int | None
    is_active: bool
    created_on: datetime
    created_by: str
    updated_on: datetime | None
    updated_by: str | None

    class ConfigDict:
        """
        Pydantic configuration to enable loading attributes 
        from ORM-style models.
        """
        from_attributes = True

class PasswordReset(BaseModel):
    """
    Model for resetting a user's password.
    """
    email: EmailStr
    current_password: str
    new_password: str
