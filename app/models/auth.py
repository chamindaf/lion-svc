from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, timezone

class Otp(Base):
    """
    SQLAlchemy model for the 'Otp' table.

    Attributes:
        otp_id (int): Primary key for the OTP entry.
        user_id (int): Foreign key linking to the 'user' table, indicating the user associated with the OTP.
        otp (str): The actual one-time password.
        attempts (int): Number of attempts made using this OTP.
        created_on (datetime): Timestamp when the OTP was created (UTC).

    Relationships:
        user (User): Relationship to the 'User' table, linking the OTP to a specific user.
    """
    __tablename__ = 'Otp'

    otp_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    otp = Column(String, nullable=False)  # Ensure OTP is not nullable
    attempts = Column(Integer, default=0, nullable=False)  # Ensure attempts is not nullable
    created_on = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship('User', foreign_keys=[user_id])
