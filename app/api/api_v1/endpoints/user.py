from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import get_users, create_user, update_user, get_user_by_id
from app.api.deps import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/get_all", response_model=List[UserRead])
def read_user(
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
    
    users = get_users(db)
    if not users:
        logger.info("No users found in the database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    
    logger.info(f"Fetched {len(users)} users successfully.")
    return users

@router.post("/create", response_model=UserRead)
def create_new_user(
    user_in: UserCreate,
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
    
    user = create_user(db, user_in, created_by=current_user.email)
    
    logger.info(f"User created with email {user.email}.")
    return user

@router.put("/update", response_model=UserRead)
def update_existing_user(
    user_in: UserUpdate,
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
    
    user = update_user(db, user_in.user_id, user_in)
    if not user:
        logger.info(f"User with ID {user_in.user_id} not found for update.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    logger.info(f"User with ID {user_in.user_id} updated successfully.")
    return user

@router.get("/by_id", response_model=UserRead)
def read_user_by_id(
    user_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.debug(f"Received request to fetch User with user id={user_id}")

    # Verify if the current user is authenticated
    if not current_user:
        logger.error("Unauthorized access attempt by user.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # Fetch lookups based on the dynamic filters
    try:
        user = get_user_by_id(db, user_id)
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching user data")

    # Handle case when no user entrie are found
    if not user:
        logger.info("No user entries found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user entries found")

    # Successfully retrieved user entries
    logger.info(f"Successfully fetched user.")
    return user
