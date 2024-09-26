from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.schemas.request_type import RequestTypeRead
from app.crud.request_type import get_unique_request_types, get_request_types
from app.api.deps import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/get_all_unique", response_model=List[RequestTypeRead])
def read_request_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users. Requires authentication.

    Args:
        db (Session): The database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the user is not authorized or no users are found.

    Returns:
        List[UserRead]: A list of user details.
    """
    if not current_user:
        logger.warning("Unauthorized access attempt to get all users.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    request_types = get_unique_request_types(db)
    if not request_types:
        logger.info("No request types found in the database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request types not found")
    
    logger.info(f"Fetched {len(request_types)} Request types successfully.")
    return request_types

@router.get("/get_all", response_model=List[RequestTypeRead])
def read_request_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users. Requires authentication.

    Args:
        db (Session): The database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the user is not authorized or no users are found.

    Returns:
        List[UserRead]: A list of user details.
    """
    if not current_user:
        logger.warning("Unauthorized access attempt to get all users.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    request_types = get_request_types(db)
    if not request_types:
        logger.info("No request types found in the database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request types not found")
    
    logger.info(f"Fetched {len(request_types)} Request types successfully.")
    return request_types