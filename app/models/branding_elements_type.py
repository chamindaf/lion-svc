from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Branding_Elements_Type(Base):
    __tablename__ = 'Branding_Elements_Type'

    branding_elements_type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    branding_elements_type = Column(String, nullable=False)