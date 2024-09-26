from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.lookup import LookupRead
from app.crud.lookup import get_lookup_dynamic
from app.api.deps import get_db, get_current_user
from app.models.user import User
import logging
from typing import Optional

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/by_fields", response_model=list[LookupRead])
def read_lookup(
    lookup_id: Optional[int] = Query(None, description="The ID of the lookup to retrieve"),
    category: Optional[str] = Query(None, description="The category of the lookup to filter"),
    is_active: Optional[bool] = Query(None, description="Filter lookups by active status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve lookup entries based on dynamic query parameters.

    This endpoint allows querying lookup entries by one or more of the following fields:
    - `lookup_id`: The unique identifier for the lookup entry.
    - `category`: The category of the lookup entry.
    - `is_active`: A boolean value to filter lookups based on their active status.

    If no lookup is found matching the provided filters, a 404 error is returned.

    Args:
        lookup_id (Optional[int]): The ID of the lookup to retrieve.
        category (Optional[str]): The category to filter lookups.
        is_active (Optional[bool]): Filter by active status.
        db (Session): The database session, injected by FastAPI.
        current_user (User): The currently authenticated user, injected by FastAPI.

    Returns:
        list[LookupRead]: A list of lookup entries matching the query.

    Raises:
        HTTPException: 
            - 403: If the user is unauthorized.
            - 404: If no lookup entries are found based on the provided filters.
    """
    logger.debug("Received request to fetch lookup(s) with filters: "
                 f"lookup_id={lookup_id}, category={category}, is_active={is_active}")

    # Verify if the current user is authenticated
    if not current_user:
        logger.warning("Unauthorized access attempt by user.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # Fetch lookups based on the dynamic filters
    try:
        lookups = get_lookup_dynamic(db, lookup_id=lookup_id, category=category, is_active=is_active)
    except Exception as e:
        logger.error(f"Error fetching lookups: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching lookup data")

    # Handle case when no lookup entries are found
    if not lookups:
        logger.info("No lookup entries found for provided filters.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No lookup entries found")

    # Successfully retrieved lookup entries
    logger.info(f"Successfully fetched {len(lookups)} lookup(s) based on the provided filters.")
    return lookups
