from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    """
    Model representing authentication tokens.

    Attributes:
        access_token (str): The token used for accessing protected resources.
        refresh_token (str): The token used for generating a new access token.
        token_type (str): The type of token (typically 'Bearer').
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenRequest(BaseModel):
    """
    Model for token requests using email and OTP.

    Attributes:
        email (EmailStr): The user's email address, validated as an email string.
        otp (int): The one-time password provided for authentication.
    """
    email: EmailStr
    otp: int

class OTP(BaseModel):
    """
    Model representing a one-time password (OTP) entity.

    Attributes:
        otp_id (Optional[int]): The unique identifier for the OTP. Optional as it may be None for new OTPs.
        user_id (int): The ID of the user associated with the OTP.
        otp (str): The actual one-time password.
        attempts (int): The number of attempts made using this OTP.
        created_on (datetime): The timestamp when the OTP was created.
    """
    otp_id: Optional[int] = None
    user_id: int
    otp: str
    attempts: int
    created_on: datetime

    class Config:
        from_attributes = True

class OTPRequest(BaseModel):
    """
    Model for OTP requests using email and password.

    Attributes:
        email (EmailStr): The user's email address, validated as an email string.
        password (str): The password of the user.
    """
    email: EmailStr
    password: str

class OTPResponse(BaseModel):
    """
    Model representing the response for OTP-related operations.

    Attributes:
        otp_id (Optional[int]): The unique identifier for the OTP. Optional as it may be None for new OTPs.
        user_id (int): The ID of the user associated with the OTP.
        attempts (int): The number of attempts made using this OTP.
        created_on (datetime): The timestamp when the OTP was created.
    """
    otp_id: Optional[int] = None
    user_id: int
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_is_active: bool
    is_temp_password: bool
    attempts: int
    created_on: datetime

    class Config:
        from_attributes = True
