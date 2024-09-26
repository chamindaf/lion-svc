from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.request import Request
from app.models.req_branding_elements_type import Req_Branding_Elements_Type
from datetime import datetime, timezone

class Branding_Elements(Base):
    __tablename__ = 'Branding_Elements'

    branding_element_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    req_branding_elements_type_id = Column(Integer, ForeignKey('Request_Branding_Elements_Type.req_branding_elements_type_id'), nullable=False)
    request_id = Column(Integer, ForeignKey('request.request_id'), nullable=False)
    branding_element = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=True)
    created_on = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    fk_request = relationship(
        'Request',
        primaryjoin=request_id == Request.request_id,
        foreign_keys=[request_id]
    )
    fk_branding_elements = relationship(
        'Req_Branding_Elements_Type',
        primaryjoin=req_branding_elements_type_id == Req_Branding_Elements_Type.req_branding_elements_type_id,
        foreign_keys=[req_branding_elements_type_id]
    )
    