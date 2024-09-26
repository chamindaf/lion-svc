from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
import logging
from pydantic import ValidationError
from app.crud.user import get_user_by_email, reset_password
from app.crud.auth import create_otp, get_otp_by_user, delete_otp
from app.core.auth import create_access_token, create_refresh_token, decode_token
from app.core.otp_security import verify_otp
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token, TokenRequest, OTPRequest, OTPResponse
from app.schemas.user import PasswordReset, UserRead
from app.api.deps import verify_user_credentials, get_current_user

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.post("/login/otp", response_model=OTPResponse)
def login(
    db: Session = Depends(get_db),
    form_data: OTPRequest = Body(...)
):
    """
    Generate an OTP for user login. Requires user credentials.

    Args:
        db (Session): The database session.
        form_data (OTPRequest): The form data containing email and password.

    Raises:
        HTTPException: If credentials are incorrect or if there is an issue sending the OTP.

    Returns:
        OTPResponse: The generated OTP.
    """
    try:
        # Verify user credentials
        user = verify_user_credentials(email=form_data.email, password=form_data.password, db=db)

        if not user:
            logger.warning("Failed login attempt: User not found or incorrect credentials.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Generate and save OTP
        otp_data = create_otp(db, user)
        logger.info(f"OTP generated and sent to user {user.email}.")
        return OTPResponse(
            otp_id=otp_data.otp_id,
            user_id=user.user_id,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            user_is_active=user.is_active,
            is_temp_password=user.is_temp_password,
            attempts=otp_data.attempts,
            created_on=otp_data.created_on
        )
    except ValidationError as e:
        # Handle validation errors gracefully
        logger.error(f"Validation error: {e.title}")
        print(f"Validation error: {e.title}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.title
        )

@router.post("/login/access_token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: TokenRequest = Body(...)
):
    """
    Generate access and refresh tokens after validating OTP.

    Args:
        db (Session): The database session.
        form_data (TokenRequest): The form data containing email and OTP.

    Raises:
        HTTPException: If OTP is incorrect or expired, or if user is not found.

    Returns:
        Token: The access and refresh tokens.
    """
    user = get_user_by_email(db, email=form_data.email)
    if not user:
        logger.warning(f"User not found for email {form_data.email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
        )
    
    otp = get_otp_by_user(db, user.user_id)
    if not otp:
        logger.warning(f"OTP not found for user {form_data.email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OTP not found",
        )
    
    if not verify_otp(db, form_data.otp, otp):
        logger.warning(f"Failed login attempt: Incorrect or expired OTP for email {form_data.email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect or expired OTP",
        )
    
    # Clear OTP after successful validation
    delete_otp(db, otp.otp_id)
    
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    
    logger.info(f"Access and refresh tokens generated for user {user.email}.")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/login/reset_password", response_model=UserRead)
def reset_password_endpoint(
    db: Session = Depends(get_db),
    form_data: PasswordReset = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Reset user password. Requires authentication.

    Args:
        db (Session): The database session.
        form_data (PasswordReset): The form data containing email, current password, and new password.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: If user is not authorized or if credentials are incorrect.

    Returns:
        UserRead: The user details after password reset.
    """
    if not current_user:
        logger.warning("Unauthorized attempt to reset password.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    
    # Verify current user credentials
    user = verify_user_credentials(email=form_data.email, password=form_data.current_password, db=db)
    
    if not user:
        logger.warning(f"Password reset attempt failed: Incorrect current password for email {form_data.email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password",
        )
    
    user = reset_password(db, user, form_data.new_password)
    logger.info(f"Password reset successfully for user {user.email}.")
    return user

@router.post("/login/refresh_token", response_model=Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using a valid refresh token.

    Args:
        refresh_token (str): The refresh token to validate and use for generating a new access token.
        db (Session): The database session.

    Raises:
        HTTPException: If the refresh token is invalid or if user is not found.

    Returns:
        Token: The new access token.
    """
    payload = decode_token(refresh_token)
    if payload is None:
        logger.warning("Invalid refresh token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"User not found for email {email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    access_token = create_access_token({"sub": user.email})
    logger.info(f"Access token refreshed for user {user.email}.")
    return {"access_token": access_token, "token_type": "bearer"}
