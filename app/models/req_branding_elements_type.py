from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.request_type import Request_Type
from app.models.branding_elements_type import Branding_Elements_Type
from datetime import datetime, timezone

class Req_Branding_Elements_Type(Base):
    __tablename__ = 'Request_Branding_Elements_Type'
    
    req_branding_elements_type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    request_type_id = Column(Integer, ForeignKey('Request_Type.request_type_id'), nullable=False)
    request_type = Column(String, nullable=False)
    branding_elements_type_id = Column(Integer, ForeignKey('Branding_Elements_Type.branding_elements_type_id'), nullable=False)
    branding_elements_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(String, nullable=True)
    created_on = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_by = Column(String, nullable=True)
    updated_on = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    #Relatonships
    fk_request_type = relationship('Request_Type', foreign_keys=[request_type_id])
    fk_branding_elements_type = relationship('Branding_Elements_Type', foreign_keys=[branding_elements_type_id])

    # Composite Unique Constraint to ensure request_type_id and branding_elements_type_id combination is unique
    __table_args__ = (UniqueConstraint('request_type_id', 'branding_elements_type_id', name='_request_branding_elements_type_uc'),)