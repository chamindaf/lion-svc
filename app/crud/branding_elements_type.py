from sqlalchemy.orm import Session
from app.models.branding_elements_type import Branding_Elements_Type
import logging
from fastapi import HTTPException, status

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_branding_element_by_id(db: Session, branding_element_type_id: int) -> Branding_Elements_Type:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Branding element to retrieve.

    Returns:
        Request_Type: The Branding element object if found, else None.
    """
    try:
        user = db.query(Branding_Elements_Type).filter(Branding_Elements_Type.branding_elements_type_id == branding_element_type_id).first()
        if user:
            logger.info(f"Branding element found with id: {branding_element_type_id}")
        else:
            logger.info(f"No Branding element found with id: {branding_element_type_id}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving Branding element with id {branding_element_type_id}: {e}")
        raise

def get_branding_elements_types(db: Session):
    """
    Retrieve a list of users from the database.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        List[User]: A list of User objects.
    """
    try:
        branding_elements_types = db.query(Branding_Elements_Type).all()
        logger.info(f"Retrieved {len(branding_elements_types)} branding element types from the database.")
        return branding_elements_types
    except Exception as e:
        logger.error(f"Error retrieving branding elements types: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
def get_branding_element_by_branding_element_type(db: Session, branding_element_type: str) -> Branding_Elements_Type:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Branding element to retrieve.

    Returns:
        Request_Type: The Branding element object if found, else None.
    """
    try:
        user = db.query(Branding_Elements_Type).filter(Branding_Elements_Type.branding_elements_type == branding_element_type).first()
        if user:
            logger.info(f"Branding element type found for: {branding_element_type}")
        else:
            logger.info(f"No Branding element type found for: {branding_element_type}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving Branding element type found for {branding_element_type}: {e}")
        raise