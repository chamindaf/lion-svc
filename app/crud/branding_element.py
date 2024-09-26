from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.branding_element import Branding_Elements
from app.schemas.branding_element import BrandingElementCreate, BrandingElementRead
import logging
from typing import List

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_branding_elements_by_request(db: Session, request_id: int, skip: int = 0, limit: int = None) -> List[BrandingElementRead]:
    """
    Retrieve a list of Request Branding Elements Types from the database.

    Args:
        db (Session): The database session.
        request_id (int): The ID of the request to filter by.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        List[BrandingElementRead]: A list of Request Branding Elements Type objects.
    """
    try:
        query = db.query(Branding_Elements).filter(Branding_Elements.request_id == request_id).offset(skip)
        
        if limit is not None:
            query = query.limit(limit)
        
        branding_elements = query.all()
        
        pydantic_branding_elements = [
            BrandingElementRead(
                branding_element_id=element.branding_element_id,
                req_branding_elements_type=element.fk_branding_elements.branding_elements_type if element.fk_branding_elements else None,
                request_id=element.request_id,
                branding_element=element.branding_element,
                created_on=element.created_on,
                created_by=element.created_by
            )
            for element in branding_elements
        ]
        
        logger.info(f"Retrieved {len(pydantic_branding_elements)} branding elements from the database.")
        return pydantic_branding_elements
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving Branding Elements: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
def create_branding_element(db: Session, branding_element_in: BrandingElementCreate, created_by: str) -> BrandingElementRead:
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
        # Create a new record
        db_branding_element = Branding_Elements(
            req_branding_elements_type_id=branding_element_in.req_branding_elements_type_id,
            request_id=branding_element_in.request_id,
            branding_element=branding_element_in.branding_element,
            created_by=created_by
        )
        db.add(db_branding_element)
        db.commit()
        db.refresh(db_branding_element)
        
        logger.info("Branding Element created successfully.")
        return BrandingElementRead(
            branding_element_id=db_branding_element.branding_element_id,
            req_branding_elements_type=db_branding_element.fk_branding_elements.branding_elements_type if db_branding_element.fk_branding_elements else None,
            request_id=db_branding_element.request_id,
            branding_element=db_branding_element.branding_element,
            created_on=db_branding_element.created_on,
            created_by=db_branding_element.created_by
            )
    except IntegrityError as e:
        logger.error(f"Integrity error while creating record: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")
    except SQLAlchemyError as e:
        logger.error(f"Error creating record: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")