from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.lookup import Lookup
from typing import Optional, List
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_lookup_dynamic(
    db: Session, 
    lookup_id: Optional[int] = None, 
    category: Optional[str] = None, 
    display_value: Optional[str] = None, 
    is_active: Optional[bool] = None
) -> List[Lookup]:
    """
    Dynamically fetch lookup entries from the database based on the provided filters.

    This function allows querying the `Lookup` table by the following optional parameters:
    - `lookup_id`: Filter by the unique identifier of the lookup.
    - `category`: Filter by the category of the lookup.
    - `is_active`: Filter by the active status of the lookup.

    Args:
        db (Session): The database session used for querying.
        lookup_id (Optional[int]): Optional filter for lookup ID.
        category (Optional[str]): Optional filter for lookup category.
        is_active (Optional[bool]): Optional filter for active status.

    Returns:
        List[Lookup]: A list of lookup entries that match the filters.

    Raises:
        SQLAlchemyError: If an error occurs during the database query.
    """
    try:
        logger.debug(f"Building dynamic query for lookups with filters: "
                     f"lookup_id={lookup_id}, category={category}, display value={display_value}, is_active={is_active}")

        # Initialize the base query
        query = db.query(Lookup)

        # Apply filters dynamically based on provided arguments
        if lookup_id is not None:
            logger.debug(f"Adding filter for lookup_id: {lookup_id}")
            query = query.filter(Lookup.lookup_id == lookup_id)
        
        if category is not None:
            logger.debug(f"Adding filter for category: {category}")
            query = query.filter(Lookup.category == category)
        
        if display_value is not None:
            logger.debug(f"Adding filter for display value: {display_value}")
            query = query.filter(Lookup.display_value == display_value)

        if is_active is not None:
            logger.debug(f"Adding filter for is_active: {is_active}")
            query = query.filter(Lookup.is_active == is_active)

        # Execute the query and retrieve all matching records
        lookups = query.all()

        logger.info(f"Query executed successfully, fetched {len(lookups)} lookup(s).")
        return lookups

    except SQLAlchemyError as e:
        logger.error(f"Error occurred while fetching lookup data: {e}")
        raise SQLAlchemyError("Database query failed.") from e
