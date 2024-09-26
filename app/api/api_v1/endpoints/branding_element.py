from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.schemas.branding_element import BrandingElementRead, BrandingElementCreate
from app.crud.branding_element import get_branding_elements_by_request, create_branding_element
from app.api.deps import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/get_all", response_model=List[BrandingElementRead])
def read_branding_elements(
    skip: int = 0,  # Pagination: records to skip
    limit: int = None,  # Pagination: max records to return
    request_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all branding element types with pagination. Requires authentication.
    """
    if not current_user:
        logger.warning("Unauthorized access attempt to get all users.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    branding_element = get_branding_elements_by_request(db, request_id=request_id, skip=skip, limit=limit)
    if not branding_element:
        logger.info("No branding elements found in the database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branding element not found")
    
    logger.info(f"Fetched {len(branding_element)} branding element successfully.")
    return branding_element

@router.post("/create", response_model=BrandingElementRead)
def create_new_branding_element(
    branding_element_in: BrandingElementCreate,
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
    
    request = create_branding_element(db, branding_element_in, created_by=current_user.email)
    
    logger.info(f"Branding Element created.")
    return request