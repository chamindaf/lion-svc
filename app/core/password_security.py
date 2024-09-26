from passlib.context import CryptContext
import random
import string
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

# Create a password context with bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.

    Raises:
        Exception: If an error occurs during hashing.
    """
    try:
        hashed = pwd_context.hash(password)
        logger.debug("Password hashed successfully.")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.

    Raises:
        Exception: If an error occurs during verification.
    """
    try:
        is_valid = pwd_context.verify(plain_password, hashed_password)
        if is_valid:
            logger.debug("Password verification successful.")
        else:
            logger.debug("Password verification failed.")
        return is_valid
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        raise

def temp_password(length=12) -> str:
    """
    Generate a temporary password with a mix of letters, digits, and symbols.

    Args:
        length (int): The length of the temporary password. Default is 12.

    Returns:
        str: The generated temporary password.

    Raises:
        Exception: If an error occurs during password generation.
    """
    try:
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        temp_pwd = ''.join(random.choice(characters) for _ in range(length))
        logger.debug(f"Temporary password generated: {temp_pwd}")
        return temp_pwd
    except Exception as e:
        logger.error(f"Error generating temporary password: {e}")
        raise
