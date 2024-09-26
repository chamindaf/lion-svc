import jwt
from datetime import datetime, timedelta, timezone
import logging
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# Set up logging for this module
logger = logging.getLogger(__name__)

def create_access_token(data: dict, token_expiration: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Create an access token with an expiration time.

    Args:
        data (dict): The data to encode in the token.
        token_expiration (int): The number of minutes until the token expires. Default is `ACCESS_TOKEN_EXPIRE_MINUTES`.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(token_expiration))
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.debug(f"Access token created with expiration: {expire}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        raise

def create_refresh_token(data: dict, token_expiration: int = REFRESH_TOKEN_EXPIRE_DAYS) -> str:
    """
    Create a refresh token with an expiration time.

    Args:
        data (dict): The data to encode in the token.
        token_expiration (int): The number of days until the token expires. Default is `REFRESH_TOKEN_EXPIRE_DAYS`.

    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=int(token_expiration))
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.debug(f"Refresh token created with expiration: {expire}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating refresh token: {e}")
        raise

def decode_token(token: str):
    """
    Decode a JWT token and return the payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded token payload if the token is valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token decoded successfully: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired.")
    except jwt.PyJWTError as e:
        logger.error(f"Error decoding token: {e}")
    return None
