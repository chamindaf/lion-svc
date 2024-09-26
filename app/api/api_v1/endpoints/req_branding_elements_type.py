from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.schemas.req_branding_elements_type import ReqBrandingElementsTypeRead, ReqBrandingElementsTypeCreate, ReqBrandingElementsTypeUpdate
from app.crud.req_branding_elements_type import get_req_branding_elements_types, create_req_branding_elements_types, update_req_branding_elements_types
from app.crud.request_type import get_request_type_by_request_type
from app.crud.branding_elements_type import get_branding_element_by_branding_element_type
from app.api.deps import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/get_all", response_model=List[ReqBrandingElementsTypeRead])
def read_req_branding_elements_types(
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
    
    req_branding_elements_types = get_req_branding_elements_types(db, skip=skip, limit=limit)

    if not req_branding_elements_types:
        logger.info("No branding elements found in the database.")
        return [{
            "req_branding_elements_type_id":0,
            "request_type_id":0,
            "request_type":"",
            "branding_elements_type_id":0,
            "branding_elements_type":"",
            "is_active":False,
            "created_on":None,
            "created_by":""
        }]
    
    logger.info(f"Fetched {len(req_branding_elements_types)} request branding elements successfully.")
    return req_branding_elements_types


@router.post("/create", response_model=ReqBrandingElementsTypeRead)
def create_req_branding_elements_type(
    req_branding_elements_type_in: ReqBrandingElementsTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new branding elements type. Requires authentication.
    """
    if not current_user:
        logger.warning("Unauthorized attempt to create a new record.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Ensure valid foreign keys (request_type and branding_elements_type)
    request_type = get_request_type_by_request_type(db=db, outlet_type=req_branding_elements_type_in.outlet_type, request_type=req_branding_elements_type_in.request_type)
    branding_element_type = get_branding_element_by_branding_element_type(db, req_branding_elements_type_in.branding_elements_type)

    req_branding_elements_type_in = ReqBrandingElementsTypeCreate(
        outlet_type=req_branding_elements_type_in.outlet_type,
        request_type_id=request_type.request_type_id,
        request_type=req_branding_elements_type_in.request_type,
        branding_elements_type_id=branding_element_type.branding_elements_type_id,
        branding_elements_type=req_branding_elements_type_in.branding_elements_type
    )
    
    req_branding_elements_type = create_req_branding_elements_types(db, req_branding_elements_type_in, created_by=current_user.email)
    logger.info(f"Request branding elements type created with ID {req_branding_elements_type.req_branding_elements_type_id}.")
    return req_branding_elements_type


@router.put("/update", response_model=ReqBrandingElementsTypeRead)
def update_req_branding_elements_type(
    req_branding_elements_type_in: ReqBrandingElementsTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update branding element type by ID. Requires authentication.
    """
    if not current_user:
        logger.warning("Unauthorized attempt to update branding elements type.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Check if the branding elements type exists before updating
    branding_element = update_req_branding_elements_types(
        db, 
        req_branding_elements_type_in.req_branding_elements_type_id, 
        req_branding_elements_type_in
    )
    
    if not branding_element:
        logger.info(f"Branding elements type with ID {req_branding_elements_type_in.req_branding_elements_type_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branding elements type not found")
    
    logger.info(f"Branding elements type with ID {req_branding_elements_type_in.req_branding_elements_type_id} updated successfully.")
    return branding_element
