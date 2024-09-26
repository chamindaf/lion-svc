from sqlalchemy.orm import Session
from app.models.request_type import Request_Type
import logging
from fastapi import status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_request_type_by_id(db: Session, request_type_id: int) -> Request_Type:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Request type to retrieve.

    Returns:
        Request_Type: The Request type object if found, else None.
    """
    try:
        user = db.query(Request_Type).filter(Request_Type.request_type_id == request_type_id).first()
        if user:
            logger.info(f"Request type found with id: {request_type_id}")
        else:
            logger.info(f"No Request type found with id: {request_type_id}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving Request type with id {request_type_id}: {e}")
        raise

def get_request_type_by_request_type(db: Session, request_type: str, outlet_type: str = None) -> Request_Type:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Request type to retrieve.

    Returns:
        Request_Type: The Request type object if found, else None.
    """
    try:
        query = db.query(Request_Type).filter(Request_Type.request_type == request_type)

        if outlet_type is not None:
            logger.debug(f"Adding filter for outlet type: {outlet_type}")
            query = query.filter(Request_Type.outlet_type == outlet_type)

        request_type = query.first()

        if request_type:
            logger.info(f"Request type found for: {request_type}")
        else:
            logger.info(f"No Request type found for: {request_type}")
        return request_type
    except Exception as e:
        logger.error(f"Error retrieving Request type for {request_type}: {e}")
        raise

def get_unique_request_types(db: Session):
    """
    Retrieve a list of unique request types from the database based on the `request_type`.

    Args:
        db (Session): The database session.

    Returns:
        List[Request_Type]: A list of unique Request_Type objects.
    """
    try:            
        # Subquery to get the first occurrence of each unique request_type
        subquery = (
            db.query(
                func.min(Request_Type.request_type_id).label("min_id")
            )
            .group_by(Request_Type.request_type)
            .subquery()
        )

        # Use the subquery to get the full records with the unique request_type
        request_types = (
            db.query(Request_Type)
            .join(subquery, Request_Type.request_type_id == subquery.c.min_id)
            .all()
        )

        logger.info(f"Retrieved {len(request_types)} unique request types from the database.")
        return request_types
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving unique request types: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def get_request_types(db: Session):
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
        request_types = db.query(Request_Type).all()
        logger.info(f"Retrieved {len(request_types)} request types from the database.")
        return request_types
    except Exception as e:
        logger.error(f"Error retrieving request_types: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")