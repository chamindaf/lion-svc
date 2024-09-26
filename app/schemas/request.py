from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssigneeInfo(BaseModel):
    tm_email: Optional[str] = None
    tm_first_name: Optional[str] = None
    tm_last_name: Optional[str] = None
    fsm_email: Optional[str] = None
    cdm_email: Optional[str] = None
    cdm_first_name: Optional[str] = None
    cdm_last_name: Optional[str] = None
    designer_email: Optional[str] = None
    designer_first_name: Optional[str] = None
    designer_last_name: Optional[str] = None
    supplier_email: Optional[str] = None
    supplier_first_name: Optional[str] = None
    supplier_last_name: Optional[str] = None
    auditor_email: Optional[str] = None
    auditor_first_name: Optional[str] = None
    auditor_last_name: Optional[str] = None
    bm_email: Optional[str] = None

class PRPOInfo(BaseModel):
    pr_number_designer: Optional[int] = None
    pr_date_designer: Optional[datetime] = None
    po_number_designer: Optional[int] = None
    po_date_designer: Optional[datetime] = None
    quotation_value_designer: Optional[float] = None
    pr_number_supplier: Optional[int] = None
    pr_date_supplier: Optional[datetime] = None
    po_number_supplier: Optional[int] = None
    po_date_supplier: Optional[datetime] = None
    quotation_value_supplier: Optional[float] = None

class Timestamps(BaseModel):
    artwork_approved_on: Optional[datetime] = None
    measurement_completed_on: Optional[datetime] = None
    quotation_received_on: Optional[datetime] = None
    work_completed_on: Optional[datetime] = None
    tm_signed_off_on: Optional[datetime] = None
    cdm_signed_off_on: Optional[datetime] = None
    hod_approved_on: Optional[datetime] = None

class BaseQuestionsInfo(BaseModel):
    bq_outlet_volume: Optional[int] = None
    bq_competitor_threat_id: Optional[int] = None
    bq_is_strategic_location: Optional[bool] = None
    bq_consumer_profile: Optional[str] = None
    bq_last_cost_incurred: Optional[float] = None
    bq_portfolio_share: Optional[float] = None
    bq_is_design_with_boq: Optional[bool] = None
    bq_sales_volume: Optional[int] = None

class RequestContact(BaseModel):
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_address: Optional[str] = None
    contact_number: Optional[int] = None

class RequestBase(AssigneeInfo, PRPOInfo, Timestamps, BaseQuestionsInfo, RequestContact):
    request_id: int
    is_new_outlet: bool
    request_type_id: int
    outlet_info_id: Optional[int] = None
    rt_code: Optional[str] = None
    channel_info_id: Optional[int] = None
    outlet_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    address_line4: Optional[str] = None
    address_line5: Optional[str] = None
    drive_brand_id: Optional[int] = None
    is_chain_outlet: Optional[bool] = None
    chain_name: Optional[str] = None
    is_urgent: Optional[bool] = None
    status_id: int
    stage_id: Optional[int] = None

class RequestRead(AssigneeInfo, PRPOInfo, Timestamps, BaseQuestionsInfo, RequestContact):
    request_id: int
    is_new_outlet: bool
    request_type: str
    outlet_info_id: Optional[int] = None
    rt_code: Optional[str] = None
    territory: Optional[str] = None
    channel: Optional[str] = None
    outlet_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    address_line4: Optional[str] = None
    address_line5: Optional[str] = None
    brand: Optional[str] = None
    is_chain_outlet: Optional[bool] = None
    chain_name: Optional[str] = None
    is_urgent: Optional[bool] = None
    status: str
    stage: Optional[str] = None

    class Config:
        """
        Pydantic configuration to enable loading attributes 
        from ORM-style models.
        """
        from_attributes = True
    
class RequestCreate(AssigneeInfo, PRPOInfo, Timestamps, BaseQuestionsInfo, RequestContact):
    is_new_outlet: bool
    request_type: str
    rt_code: str
    territory: str
    channel: str
    outlet_name: str
    address_line1: str
    address_line2: str
    address_line3: Optional[str] = None
    address_line4: Optional[str] = None
    address_line5: Optional[str] = None
    brand: str
    is_chain_outlet: bool
    chain_name: Optional[str] = None
    is_urgent: bool
    status: str
    stage: Optional[str] = None

class RequestCreateResponse(AssigneeInfo, BaseQuestionsInfo, RequestContact):
    request_id: Optional[int] = None
    is_new_outlet: bool
    request_type_id: int
    request_type: str
    outlet_info_id: Optional[int] = None
    rt_code: Optional[str] = None
    territory_info_id: Optional[int] = None
    channel_info_id: Optional[int] = None
    outlet_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    address_line4: Optional[str] = None
    address_line5: Optional[str] = None
    drive_brand_id: Optional[int] = None
    is_chain_outlet: Optional[bool] = None
    chain_name: Optional[str] = None
    is_urgent: Optional[bool] = None
    status_id: int
    status: str
    stage_id: Optional[int] = None

    class Config:
        """
        Pydantic configuration to enable loading attributes 
        from ORM-style models.
        """
        Oorm_mode = True

class RequestUpdate(AssigneeInfo, PRPOInfo, Timestamps, BaseQuestionsInfo, RequestContact):
    request_id: int
    rt_code: Optional[str] = None
    territory: Optional[str] = None
    channel: Optional[str] = None
    outlet_name: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    address_line4: Optional[str] = None
    address_line5: Optional[str] = None
    brand: Optional[str] = None
    is_chain_outlet: Optional[bool] = None
    chain_name: Optional[str] = None
    status: str
    stage: Optional[str] = None