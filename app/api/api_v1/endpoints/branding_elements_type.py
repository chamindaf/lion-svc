from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
from app.schemas.branding_elements_type import BrandingElementsTypeRead
from app.crud.branding_elements_type import get_branding_elements_types
from app.api.deps import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/get_all", response_model=List[BrandingElementsTypeRead])
def read_branding_elements_types(
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
    
    branding_elements_types = get_branding_elements_types(db=db)
    if not branding_elements_types:
        logger.info("No branding elements types found in the database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="branding elements types not found")
    
    logger.info(f"Fetched {len(branding_elements_types)} branding elements types successfully.")
    return branding_elements_types