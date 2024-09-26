from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.sf_tables import TerritoryInfo, ChannelInfo, ChainInfo, OutletInfo, BrandInfo
from app.models.user import User
from app.models.lookup import Lookup
from app.models.request_type import Request_Type

class Request(Base):
    __tablename__ = 'request'

    request_id = Column(Integer, primary_key=True)
    is_new_outlet = Column(Boolean)
    request_type_id = Column(Integer, ForeignKey('Request_Type.request_type_id'))
    outlet_info_id = Column(Integer, ForeignKey('outlet_info.outlet_info_id'))
    rt_code = Column(String(8))
    territory_info_id = Column(Integer, ForeignKey('territory_info.territory_info_id'))
    channel_info_id = Column(Integer, ForeignKey('channel_info.channel_info_id'))
    outlet_name = Column(String(40))
    address_line1 = Column(String(40))
    address_line2 = Column(String(40))
    address_line3 = Column(String(40))
    address_line4 = Column(String(40))
    address_line5 = Column(String(40))
    drive_brand_id = Column(Integer, ForeignKey('brand_info.brand_info_id'))
    is_chain_outlet = Column(Boolean)
    chain_name = Column(String(40))
    is_urgent = Column(Boolean)
    status_id = Column(Integer, ForeignKey('lookup.lookup_id'))
    stage_id = Column(Integer, ForeignKey('lookup.lookup_id'))
    contact_name = Column(String(40))
    contact_email = Column(String(40))
    contact_address = Column(String(40))
    contact_number = Column(Integer)
    bq_outlet_volume = Column(Integer)
    bq_competitor_threat_id = Column(Integer)
    bq_is_strategic_location = Column(Boolean)
    bq_consumer_profile = Column(String(40))
    bq_last_cost_incurred = Column(Float(10, 2))
    bq_portfolio_share = Column(Float(10, 2))
    bq_is_design_with_boq = Column(Boolean)
    bq_sales_volume = Column(Integer)
    tm_email = Column(String(40), ForeignKey('user.email'))
    fsm_email = Column(String(40))
    cdm_email = Column(String(40), ForeignKey('user.email'))
    designer_email = Column(String(40), ForeignKey('user.email'))
    supplier_email = Column(String(40), ForeignKey('user.email'))
    auditor_email = Column(String(40), ForeignKey('user.email'))
    bm_email = Column(String(40))
    pr_number_designer = Column(Integer)
    pr_date_designer = Column(DateTime)
    po_number_designer = Column(Integer)
    po_date_designer = Column(DateTime)
    quotation_value_designer = Column(Float(10, 2))
    pr_number_supplier = Column(Integer)
    pr_date_supplier = Column(DateTime)
    po_number_supplier = Column(Integer)
    po_date_supplier = Column(DateTime)
    quotation_value_supplier = Column(Float(10, 2))
    artwork_approved_on = Column(DateTime)
    measurement_completed_on = Column(DateTime)
    quotation_received_on = Column(DateTime)
    work_completed_on = Column(DateTime)
    tm_signed_off_on = Column(DateTime)
    cdm_signed_off_on = Column(DateTime)
    hod_approved_on = Column(DateTime)

    # Correct relationships
    fk_request_type = relationship(
        'Request_Type',
        primaryjoin=request_type_id == Request_Type.request_type_id,
        foreign_keys=[request_type_id]
    )
    fk_outlet_info = relationship(
        'OutletInfo',
        primaryjoin=outlet_info_id == OutletInfo.outlet_info_id,
        foreign_keys=[outlet_info_id]
    )
    fk_territory_info = relationship(
        'TerritoryInfo',
        primaryjoin=territory_info_id == TerritoryInfo.territory_info_id,
        foreign_keys=[territory_info_id]
    )
    fk_channel_info = relationship(
        'ChannelInfo',
        primaryjoin=channel_info_id == ChannelInfo.channel_info_id,
        foreign_keys=[channel_info_id]
    )
    fk_drive_brand = relationship(
        'BrandInfo',
        primaryjoin=drive_brand_id == BrandInfo.brand_info_id,
        foreign_keys=[drive_brand_id]
    )
    fk_status_lookup = relationship(
        'Lookup',
        primaryjoin=status_id == Lookup.lookup_id,
        foreign_keys=[status_id],
        uselist=False
    )
    fk_stage_lookup = relationship(
        'Lookup',
        primaryjoin=stage_id == Lookup.lookup_id,
        foreign_keys=[stage_id],
        uselist=False
    )
    fk_tm_user = relationship(
        'User',
        primaryjoin=tm_email == User.email,
        foreign_keys=[tm_email],
        uselist=False
    )
    fk_cdm_user = relationship(
        'User',
        primaryjoin=cdm_email == User.email,
        foreign_keys=[cdm_email],
        uselist=False
    )
    fk_designer_user = relationship(
        'User',
        primaryjoin=designer_email == User.email,
        foreign_keys=[designer_email],
        uselist=False
    )
    fk_supplier_user = relationship(
        'User',
        primaryjoin=supplier_email == User.email,
        foreign_keys=[supplier_email],
        uselist=False
    )
    fk_auditor_user = relationship(
        'User',
        primaryjoin=auditor_email == User.email,
        foreign_keys=[auditor_email],
        uselist=False
    )