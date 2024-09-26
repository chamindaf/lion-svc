from passlib.context import CryptContext
import random
import string
import logging
from fastapi import HTTPException, status
from app.schemas.token import OTP
from app.schemas.user import UserRead
from app.models.auth import Otp
from app.utils.otp_utils import verify_otp_attempts
from datetime import datetime, timedelta, timezone
from app.config import OTP_LENGTH, OTP_MAX_ATTEMPTS, OTP_VALID_DURATION

# Set up logging for this module
logger = logging.getLogger(__name__)

# Create a password context with bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp(db, existing_otps: list[Otp], user: UserRead, length=int(OTP_LENGTH)):
    """
    Generate a one-time password (OTP) consisting of digits.

    Args:
        db (Session): The database session.
        existing_otps (list[Otp]): List of existing OTPs in the database.
        user (UserRead): The user object for whom the OTP is being generated.
        length (int): The length of the OTP. Default is 5. Must be a positive integer.

    Returns:
        tuple: A tuple containing the generated OTP as a string and the OTP object saved in the database.

    Raises:
        ValueError: If length is less than or equal to 0.
        Exception: If there is an error during OTP generation or database operations.
    """
    if length <= 0:
        raise ValueError("Length must be a positive integer.")
    
    try:
        max_attempts = int(OTP_MAX_ATTEMPTS)
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            
            if length == 1:
                otp = random.choice(string.digits[1:])  # Only digits 1-9
            else:
                otp = random.choice(string.digits[1:]) + ''.join(random.choice(string.digits) for _ in range(length - 1))

            logger.info("Generating OTP.")

            # Hash the generated OTP
            hashed_otp = hash_otp(otp)

            # Check if the hashed OTP already exists in the database
            if existing_otps and hashed_otp in [otp.otp for otp in existing_otps]:
                logger.debug("Generated OTP already exists, trying a new one.")
                continue
            
            # Create and save the OTP in the database
            db_otp = Otp(
                user_id=user.user_id,
                otp=hashed_otp,
                created_on=datetime.now(timezone.utc)
            )
            db.add(db_otp)
            db.commit()
            db.refresh(db_otp)

            logger.info(f"OTP created successfully for User ID {user.user_id}.")
            logger.debug(f"Generated OTP: {otp}")
            return otp, db_otp
        
        raise Exception("Failed to generate a unique OTP after multiple attempts.")
    
    except Exception as e:
        logger.error(f"Error generating OTP: {e}")
        raise

def hash_otp(otp: int) -> str:
    """
    Hash a one-time password (OTP) using bcrypt.

    Args:
        otp (int): The plain number OTP to hash.

    Returns:
        str: The hashed OTP.

    Raises:
        Exception: If an error occurs during hashing.
    """
    try:
        hashed = pwd_context.hash(str(otp))
        logger.debug("OTP hashed successfully.")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing OTP: {e}")
        raise

def verify_otp(db, plain_otp: int, otp: OTP) -> bool:
    """
    Verify an OTP against a hashed OTP, checking for expiration and maximum attempts.

    Args:
        db (Session): The database session.
        plain_otp (int): The plain text OTP to verify.
        otp (OTP): The OTP object containing the hashed OTP, creation time, and attempt count.

    Returns:
        bool: True if the OTP matches, is not expired, and has not exceeded maximum attempts; False otherwise.

    Raises:
        HTTPException: If OTP verification fails due to reaching max attempts, expiration, or other issues.
    """
    # Get current time in UTC
    current_time = datetime.now(timezone.utc)

    # Ensure otp.created_on is timezone-aware
    otp_created_on = otp.created_on if otp.created_on.tzinfo else otp.created_on.replace(tzinfo=timezone.utc)

    # Verify OTP
    is_verified = pwd_context.verify(str(plain_otp), otp.otp)

    # Handle OTP verification failure and maximum attempts
    if not is_verified:
        verify_otp_attempts(db, otp)
        logger.debug("OTP verification failed.")
        return False

    # Check if OTP has expired (5 minutes)
    otp_expiry_duration = timedelta(minutes=int(OTP_VALID_DURATION))
    is_not_expired = current_time - otp_created_on < otp_expiry_duration

    # Final validation
    if is_verified and is_not_expired:
        logger.debug("OTP verification successful.")
        return True
    else:
        if not is_not_expired:
            logger.warning(f"OTP expired for OTP ID: {otp.otp_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="OTP has expired.")
        return False
    