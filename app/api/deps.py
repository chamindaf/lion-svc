from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import logging
from app.db.session import get_db
from app.models.user import User
from app.core.password_security import verify_password
from app.core.auth import decode_token
from app.crud.user import get_user_by_email

# Set up logging for this module
logger = logging.getLogger(__name__)

# OAuth2 password flow scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

def verify_user_credentials(email: str, password: str, db: Session = Depends(get_db)) -> User:
    """
    Verify user credentials and return the user if valid.

    Args:
        email (str): The email address of the user.
        password (str): The password provided by the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If user not found or password is incorrect.

    Returns:
        User: The user object if credentials are valid.
    """
    user = get_user_by_email(db, email=email)
    if not user:
        logger.warning(f"User with email {email} not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Incorrect password for user with email {email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"User with email {email} successfully authenticated.")
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieve the current user based on the JWT token.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        token (str, optional): The JWT token. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If credentials are invalid or user not found.

    Returns:
        User: The current user if the token is valid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        logger.warning("Token decoding failed or token is invalid.")
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        logger.warning("Token payload missing 'sub' field.")
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"User with email {email} not found in the database.")
        raise credentials_exception
    
    logger.info(f"User with email {email} successfully retrieved from token.")
    return user
