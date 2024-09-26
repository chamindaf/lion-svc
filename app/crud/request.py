from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.exc import SQLAlchemyError
from app.models.request import Request
from app.schemas.request import RequestRead, RequestCreate, RequestCreateResponse, RequestUpdate
from app.crud.request_type import get_request_type_by_request_type
from app.crud.sf_tables import get_territory_by_territory, get_channel_by_channel, get_brand_by_brand
from app.crud.lookup import get_lookup_dynamic
import logging
from typing import List

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_requests(db: Session, skip: int = 0, limit: int = 10) -> List[RequestRead]:
    try:
        # Building the query with eager loading for related entities
        query = db.query(Request)\
            .options(
                joinedload(Request.fk_request_type),
                joinedload(Request.fk_territory_info),
                joinedload(Request.fk_channel_info),
                joinedload(Request.fk_drive_brand),
                joinedload(Request.fk_status_lookup),
                joinedload(Request.fk_stage_lookup)
            ).offset(skip)
        
        if limit is not None:
            query = query.limit(limit)

        requests = query.all()

        # Convert SQLAlchemy models to Pydantic models for response using from_orm
        pydantic_requests = []
        for req in requests:
            pydantic_request = RequestRead(
                request_id=req.request_id,
                is_new_outlet=req.is_new_outlet,
                request_type=req.fk_request_type.request_type if req.fk_request_type else None,
                outlet_info_id=req.outlet_info_id,
                rt_code=req.rt_code,
                territory=req.fk_territory_info.territory if req.fk_territory_info else None,
                channel=req.fk_channel_info.channel if req.fk_channel_info else None,
                outlet_name=req.outlet_name,
                address_line1=req.address_line1,
                address_line2=req.address_line2,
                address_line3=req.address_line3,
                address_line4=req.address_line4,
                address_line5=req.address_line5,
                brand=req.fk_drive_brand.brand if req.fk_drive_brand else None,
                is_chain_outlet=req.is_chain_outlet,
                chain_name=req.chain_name,
                is_urgent=req.is_urgent,
                status=req.fk_status_lookup.display_value if req.fk_status_lookup else None,
                stage=req.fk_stage_lookup.display_value if req.fk_stage_lookup else None,
                contact_name=req.contact_name,
                contact_email=req.contact_email,
                contact_address=req.contact_address,
                contact_number=req.contact_number,
                bq_outlet_volume=req.bq_outlet_volume,
                bq_competitor_threat_id=req.bq_competitor_threat_id,
                bq_is_strategic_location=req.bq_is_strategic_location,
                bq_consumer_profile=req.bq_consumer_profile,
                bq_last_cost_incurred=req.bq_last_cost_incurred,
                bq_portfolio_share=req.bq_portfolio_share,
                bq_is_design_with_boq=req.bq_is_design_with_boq,
                bq_sales_volume=req.bq_sales_volume,
                tm_email=req.tm_email,
                tm_first_name=req.fk_tm_user.first_name,
                tm_lsat_name=req.fk_tm_user.last_name,
                fsm_email=req.fsm_email,
                cdm_email=req.cdm_email,
                designer_email=req.designer_email,
                supplier_email=req.supplier_email,
                auditor_email=req.auditor_email,
                bm_email=req.bm_email,
                pr_number_designer=req.pr_number_designer,
                pr_date_designer=req.pr_date_designer,
                po_number_designer=req.po_number_designer,
                po_date_designer=req.po_date_designer,
                quotation_value_designer=req.quotation_value_designer,
                pr_number_supplier=req.pr_number_supplier,
                pr_date_supplier=req.pr_date_supplier,
                po_number_supplier=req.po_number_supplier,
                po_date_supplier=req.po_date_supplier,
                quotation_value_supplier=req.quotation_value_supplier,
                artwork_approved_on=req.artwork_approved_on,
                measurement_completed_on=req.measurement_completed_on,
                quotation_received_on=req.quotation_received_on,
                work_completed_on=req.work_completed_on,
                tm_signed_off_on=req.tm_signed_off_on,
                cdm_signed_off_on=req.cdm_signed_off_on,
                hod_approved_on=req.hod_approved_on
            )
            pydantic_requests.append(pydantic_request)

        # Log and return the result
        logger.info(f"Retrieved {len(pydantic_requests)} requests from the database.")
        return pydantic_requests
    
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving Requests: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Unable to retrieve requests"
        )

def create_request(db: Session, request_in: RequestCreate, created_by: str) -> RequestCreateResponse:
    """
    Create a new Request with Branding Elements.

    Args:
        db (Session): The database session.
        request_in (RequestCreate): The input data for the new request.
        created_by (str): The user creating the new record.

    Returns:
        Request: The created Request object.
    """
    try:
        outlet_type = "New" if request_in.is_new_outlet else "Existing"
        # Ensure request_type and branding_elements_type exist
        db_request_type = get_request_type_by_request_type(db=db, outlet_type=outlet_type, request_type=request_in.request_type)
        db_territory = get_territory_by_territory(db, request_in.territory)
        db_channel = get_channel_by_channel(db, request_in.channel)
        db_brand = get_brand_by_brand(db, request_in.brand)
        db_status_lookup = get_lookup_dynamic(db=db, display_value=request_in.status)[0]
        db_stage_looukp = get_lookup_dynamic(db=db, display_value=request_in.stage)[0]

        if not (db_request_type and db_territory and db_channel and db_brand):
            raise HTTPException(status_code=400, detail="One or more related objects were not found.")

        # Create a new record
        db_request = Request(
                is_new_outlet=request_in.is_new_outlet,
                request_type_id=db_request_type.request_type_id if db_request_type else None,
                rt_code=request_in.rt_code,
                territory_info_id=db_territory.territory_info_id if db_territory else None,
                channel_info_id=db_channel.channel_info_id if db_channel else None,
                outlet_name=request_in.outlet_name,
                address_line1=request_in.address_line1,
                address_line2=request_in.address_line2,
                address_line3=request_in.address_line3,
                address_line4=request_in.address_line4,
                address_line5=request_in.address_line5,
                drive_brand_id=db_brand.brand_info_id if db_brand else None,
                is_chain_outlet=request_in.is_chain_outlet,
                chain_name=request_in.chain_name,
                is_urgent=request_in.is_urgent,
                status_id=db_status_lookup.lookup_id if db_status_lookup else None,
                stage_id=db_stage_looukp.lookup_id if db_stage_looukp else None,
                contact_name=request_in.contact_name,
                contact_email=request_in.contact_email,
                contact_address=request_in.contact_address,
                contact_number=request_in.contact_number,
                bq_outlet_volume=request_in.bq_outlet_volume,
                bq_competitor_threat_id=request_in.bq_competitor_threat_id,
                bq_is_strategic_location=request_in.bq_is_strategic_location,
                bq_consumer_profile=request_in.bq_consumer_profile,
                bq_last_cost_incurred=request_in.bq_last_cost_incurred,
                bq_portfolio_share=request_in.bq_portfolio_share,
                bq_is_design_with_boq=request_in.bq_is_design_with_boq,
                bq_sales_volume=request_in.bq_sales_volume,
                tm_email=created_by
            )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        logger.info(f"Request with ID {db_request.request_id} created successfully.")
        return RequestCreateResponse(
            request_id=db_request.request_id,
            is_new_outlet=db_request.is_new_outlet,
            request_type_id=db_request.request_type_id,
            request_type=request_in.request_type,
            outlet_name=db_request.outlet_name,
            rt_code=db_request.rt_code,
            territory_info_id=db_request.territory_info_id,
            channel_info_id=db_request.channel_info_id,
            address_line1=db_request.address_line1,
            address_line2=db_request.address_line2,
            address_line3=db_request.address_line3,
            address_line4=db_request.address_line4,
            address_line5=db_request.address_line5,
            drive_brand_id=db_request.drive_brand_id,
            is_chain_outlet=db_request.is_chain_outlet,
            chain_name=db_request.chain_name,
            is_urgent=db_request.is_urgent,
            status_id=db_request.status_id,
            status=request_in.status,
            stage_id=db_request.stage_id,
            contact_name=db_request.contact_name,
            contact_email=db_request.contact_email,
            contact_address=db_request.contact_address,
            contact_number=db_request.contact_number,
            tm_email=db_request.tm_email
        )
    except IntegrityError as e:
        logger.error(f"Integrity error while creating record: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")
    except SQLAlchemyError as e:
        logger.error(f"Error creating record: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def update_request(db: Session, request_id: int, request_update: dict) -> RequestRead:
    """
    Update a user's information in the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        user_update (dict): Dictionary containing the fields to update.

    Returns:
        User: The updated User object.

    Raises:
        HTTPException: If the user with the given ID is not found.
    """
    try:
        # Convert dict to Pydantic model if necessary
        if not isinstance(request_update, RequestUpdate):
            request_update = RequestUpdate(**request_update)

        db_user = db.query(Request).filter(Request.request_id == request_id).first()
        if db_user:
            for key, value in RequestUpdate.model_dump(exclude_unset=True).items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
            logger.info(f"Request with ID {request_id} updated successfully.")
            return db_user
        else:
            logger.warning(f"User with ID {request_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        logger.error(f"Error updating user with ID {request_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")