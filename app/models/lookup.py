from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.db.base import Base

class Lookup(Base):
    __tablename__ = 'lookup'
    
    lookup_id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    display_value = Column(String, nullable=False)
    sort = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_by = Column(String)
    created_on = Column(DateTime)
    updated_by = Column(String)
    updated_on = Column(DateTime)
