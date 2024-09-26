from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.base import Base
from datetime import datetime, timezone

class User(Base):
    """
    SQLAlchemy model for the 'user' table.

    Attributes:
    - user_id: Primary key for the user.
    - role: Role for each user.
    - email: Unique email address for the user.
    - first_name: First name of the user.
    - last_name: Last name of the user.
    - hashed_password: Securely stored hashed password for authentication.
    - is_temp_password: Flag indicating if the current password is temporary.
    - is_active: Status of the user account (active/inactive).
    - created_by: Identifier for the creator of the user record.
    - created_on: Timestamp when the user record was created (UTC).
    - updated_by: Identifier for the last updater of the user record.
    - updated_on: Timestamp when the user record was last updated (UTC).
    """
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    vendor_id = Column(Integer, nullable=False)
    company = Column(String, nullable=True)
    contact = Column(Integer, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_temp_password = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String, nullable=True)
    created_on = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_by = Column(String, nullable=True)
    updated_on = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))