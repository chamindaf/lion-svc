from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.req_branding_elements_type import Req_Branding_Elements_Type
from app.schemas.req_branding_elements_type import ReqBrandingElementsTypeCreate, ReqBrandingElementsTypeUpdate
from app.crud.branding_elements_type import get_branding_element_by_id
from app.crud.request_type import get_request_type_by_id
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_req_branding_elements_types(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of Request Branding Elements Types from the database.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        List[Req_Branding_Elements_Type]: A list of Request Branding Elements Type objects.
    """
    try:
        query = db.query(Req_Branding_Elements_Type).offset(skip)
        if limit is not None:
            query = query.limit(limit)

        req_branding_elements_types = query.all()
        
        logger.info(f"Retrieved {len(req_branding_elements_types)} request branding elements from the database.")
        return req_branding_elements_types
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving Request Branding Elements Types: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
def create_req_branding_elements_types(db: Session, req_branding_elements_type_in: ReqBrandingElementsTypeCreate, created_by: str) -> Req_Branding_Elements_Type:
    """
    Create a new Request Branding Elements Type.

    Args:
        db (Session): The database session.
        req_branding_elements_type_in (ReqBrandingElementsTypeCreate): The input data for the new branding elements type.
        created_by (str): The user creating the new record.

    Returns:
        Req_Branding_Elements_Type: The created Request Branding Elements Type object.
    """
    try:
        # Ensure request_type and branding_elements_type exist
        db_request_type = get_request_type_by_id(db, req_branding_elements_type_in.request_type_id)
        db_branding_element = get_branding_element_by_id(db, req_branding_elements_type_in.branding_elements_type_id)

        # Check for unique constraint (request_type_id + branding_elements_type_id)
        existing = db.query(Req_Branding_Elements_Type).filter(
            Req_Branding_Elements_Type.request_type_id == req_branding_elements_type_in.request_type_id,
            Req_Branding_Elements_Type.branding_elements_type_id == req_branding_elements_type_in.branding_elements_type_id
        ).first()

        if existing:
            logger.warning(f"Request Branding Elements Type with request_type_id {req_branding_elements_type_in.request_type_id} "
                           f"and branding_elements_type_id {req_branding_elements_type_in.branding_elements_type_id} already exists.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate Request Branding Elements Type")

        # Create a new record
        db_req_branding_elements_type = Req_Branding_Elements_Type(
            request_type_id=req_branding_elements_type_in.request_type_id,
            request_type=db_request_type.request_type,
            branding_elements_type_id=req_branding_elements_type_in.branding_elements_type_id,
            branding_elements_type=db_branding_element.branding_elements_type,
            is_active=False,
            created_by=created_by
        )
        db.add(db_req_branding_elements_type)
        db.commit()
        db.refresh(db_req_branding_elements_type)
        logger.info(f"Request Branding Elements Type with ID {db_req_branding_elements_type.req_branding_elements_type_id} created successfully.")
        return db_req_branding_elements_type
    except IntegrityError as e:
        logger.error(f"Integrity error while creating record: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")
    except SQLAlchemyError as e:
        logger.error(f"Error creating record: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def update_req_branding_elements_types(db: Session, req_branding_elements_type_id: int, req_branding_elements_type_update: dict) -> Req_Branding_Elements_Type:
    """
    Update a Request Branding Elements Type in the database.

    Args:
        db (Session): The database session.
        req_branding_elements_type_id (int): The ID of the Request Branding Elements Type to update.
        req_branding_elements_type_update (dict): Dictionary containing the fields to update.

    Returns:
        Req_Branding_Elements_Type: The updated Request Branding Elements Type object.

    Raises:
        HTTPException: If the Request Branding Elements Type with the given ID is not found.
    """
    try:
        # Convert dict to Pydantic model if necessary
        if not isinstance(req_branding_elements_type_update, ReqBrandingElementsTypeUpdate):
            req_branding_elements_type_update = ReqBrandingElementsTypeUpdate(**req_branding_elements_type_update)

        db_req_branding_elements_type = db.query(Req_Branding_Elements_Type).filter(
            Req_Branding_Elements_Type.req_branding_elements_type_id == req_branding_elements_type_id).first()

        if db_req_branding_elements_type:
            for key, value in req_branding_elements_type_update.model_dump(exclude_unset=True).items():
                setattr(db_req_branding_elements_type, key, value)
            db.commit()
            db.refresh(db_req_branding_elements_type)
            logger.info(f"Request Branding Elements Type with ID {req_branding_elements_type_id} updated successfully.")
            return db_req_branding_elements_type
        else:
            logger.warning(f"Request Branding Elements Type with ID {req_branding_elements_type_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request Branding Elements Type not found")
    except SQLAlchemyError as e:
        logger.error(f"Error updating Request Branding Elements Type with ID {req_branding_elements_type_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")