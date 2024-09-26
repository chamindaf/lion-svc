import logging
from fastapi import HTTPException, status
from app.schemas.token import OTP
from app.models.user import User
from app.models.auth import Otp

# Set up logging for this module
logger = logging.getLogger(__name__)

def verify_otp_attempts(db, otp: OTP):
    """
    Verify and update the OTP attempt count, handling the case where the maximum number of attempts is reached.

    Args:
        db: Database session to perform queries and operations.
        otp (OTP): OTP schema object containing the OTP ID and the number of attempts.

    Returns:
        Otp: Updated OTP object from the database.

    Raises:
        HTTPException: 403 if max attempts are reached and OTP is deleted,
                       404 if the OTP is not found,
                       500 for any internal server error.
    """
    # Check if the maximum number of attempts has been reached
    if otp.attempts >= 3:
        # Retrieve and delete OTP if max attempts are reached
        db_otp = db.query(Otp).filter(Otp.otp_id == otp.otp_id).first()
        db_user = db.query(User).filter(User.user_id == otp.user_id).first()
        if db_otp:
            db.delete(db_otp)
            db.commit()
            logger.warning(f"Max attempts reached for OTP ID: {otp.otp_id}. OTP deleted.")
            if db_user:
                setattr(db_user, "is_active", False)
                db.commit()
                logger.warning(f"User with ID {otp.user_id} deactivated.")
            else:
                logger.warning(f"User with ID {otp.user_id} not found during max attempt check.")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Max OTP attempts reached.")
        else:
            logger.warning(f"OTP with ID {otp.otp_id} not found during max attempt check.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP not found.")
    
    # Update OTP attempt count if within the limits
    db_otp = db.query(Otp).filter(Otp.otp_id == otp.otp_id).first()
    if db_otp:
        setattr(db_otp, "attempts", otp.attempts + 1)
        db.commit()
        db.refresh(db_otp)
        logger.info(f"OTP with ID {otp.otp_id} updated successfully. Attempt count: {otp.attempts + 1}.")
        return db_otp
    else:
        logger.warning(f"OTP with ID {otp.otp_id} not found during update attempt.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP not found.")
