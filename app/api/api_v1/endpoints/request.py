from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.schemas.request import RequestRead, RequestCreate, RequestUpdate
from app.crud.request import get_requests, create_request, update_request
from app.api.deps import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/get_all", response_model=List[RequestRead])
def read_requests(
    skip: int = 0,  # Pagination: records to skip
    limit: int = 10,  # Pagination: max records to return
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all branding element types with pagination. Requires authentication.
    """
    if not current_user:
        logger.warning("Unauthorized access attempt to get all users.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    requests = get_requests(db, skip=skip, limit=limit)
    if not requests:
        logger.info("No requests found in the database.")
        return [
                    {
                        "request_id": 0,
                        "is_new_outlet": False,
                        "request_type": "",
                        "outlet_info_id": 0,
                        "rt_code": "",
                        "territory": "",
                        "channel": "",
                        "outlet_name": "",
                        "address_line1": "",
                        "address_line2": "",
                        "address_line3": "",
                        "address_line4": "",
                        "address_line5": "",
                        "brand": "",
                        "is_chain_outlet": False,
                        "chain_name": "",
                        "is_urgent": False,
                        "status": "",
                        "stage": ""
                    }
                ]
    
    logger.info(f"Fetched {len(requests)} requests successfully.")
    return requests

@router.post("/create", response_model=RequestRead)
def create_new_request(
    request_in: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new user. Requires authentication.

    Args:
        user_in (UserCreate): The user data to create a new user.
        db (Session): The database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the user is not authorized or if there is an issue creating the user.

    Returns:
        UserRead: The created user details.
    """
    if not current_user:
        logger.warning("Unauthorized attempt to create a new user.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    request = create_request(db, request_in, created_by=current_user.email)
    
    logger.info(f"Request created with request type {request_in.request_type}.")
    return request

@router.put("/update", response_model=RequestRead)
def update_existing_user(
    request_in: RequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user details by user_id. Requires authentication.

    Args:
        user_in (UserUpdate): The user data to update.
        db (Session): The database session.
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the user is not authorized or if the user to update is not found.

    Returns:
        UserRead: The updated user details.
    """
    if not current_user:
        logger.warning("Unauthorized attempt to update user.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    user = update_request(db, request_in.request_id, request_in)
    if not user:
        logger.info(f"User with ID {request_in.request_id} not found for update.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    logger.info(f"User with ID {request_in.request_id} updated successfully.")
    return user