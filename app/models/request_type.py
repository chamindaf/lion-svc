from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Request_Type(Base):
    __tablename__ = 'Request_Type'

    request_type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    outlet_type = Column(String, nullable=False)
    request_type = Column(String, nullable=False)