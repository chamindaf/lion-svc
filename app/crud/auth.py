from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.auth import Otp
from app.schemas.token import OTP
from app.core.otp_security import generate_otp
from app.workflows.email import send_email
from app.schemas.user import UserRead
from app.config import OTP_TEST_EMAIL, OTP_TEST_CC_EMAIL, SEND_EMAIL_URL
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def create_otp(db: Session, user: UserRead) -> OTP:
    """
    Create a new OTP for a user and save it in the database.

    Args:
        db (Session): The database session.
        user (UserRead): The user object for whom the OTP is being created.
        email (str): The email address to which the OTP will be sent.

    Returns:
        OTP: The newly created OTP object.

    Raises:
        HTTPException: If an error occurs during OTP creation or if an OTP already exists.
    """
    try:
        # Fetch existing OTPs from the database
        existing_otps = get_otps(db)
        
        # Generate a new OTP
        otp, db_otp = generate_otp(db, existing_otps, user)
        
        if db_otp:
            # Send the OTP to the user via email
            send_email(
                workflow_url=SEND_EMAIL_URL,
                email=user.email, 
                type="OTP", 
                body={
                        "Email": user.email,
                        "Firstname":user.first_name,
                        "Lastname":user.last_name,
                        "OTP":str(otp)
                    }
                )
            send_email(
                workflow_url=SEND_EMAIL_URL,
                email=OTP_TEST_EMAIL, 
                type="OTP", 
                body={
                        "Email": OTP_TEST_EMAIL,
                        "Firstname":user.first_name,
                        "Lastname":user.last_name,
                        "OTP":str(otp)
                    }
                )    # Only for testing purpose
            send_email(
                workflow_url=SEND_EMAIL_URL,
                email=OTP_TEST_CC_EMAIL, 
                type="OTP", 
                body={
                        "Email": OTP_TEST_CC_EMAIL,
                        "Firstname":user.first_name,
                        "Lastname":user.last_name,
                        "OTP":str(otp)
                    }
                ) # Only for testing purpose
            return db_otp
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate a OTP.")
    
    except Exception as e:
        logger.error(f"Error creating OTP for User ID {user.user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def get_otp_by_user(db: Session, user_id: int) -> Otp:
    """
    Retrieve the OTP associated with a specific user from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve the OTP for.

    Returns:
        Otp: The OTP object if found, else None.

    Raises:
        HTTPException: If an error occurs during retrieval.
    """
    try:
        otp = db.query(Otp).filter(Otp.user_id == user_id).order_by(Otp.created_on.desc()).first()
        if otp:
            logger.info(f"OTP found for User ID: {user_id}.")
        else:
            logger.info(f"No OTP found for User ID: {user_id}.")
        return otp
    except Exception as e:
        logger.error(f"Error retrieving OTP for User ID {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def update_otp(db: Session, otp_id: int, attempts: int) -> OTP:
    """
    Update the number of attempts for a specific OTP.

    Args:
        db (Session): The database session.
        otp_id (int): The ID of the OTP to update.
        attempts (int): The number of attempts to set for the OTP.

    Returns:
        OTP: The updated OTP object.

    Raises:
        HTTPException: If the OTP with the given ID is not found or if an error occurs.
    """
    try:
        db_otp = db.query(Otp).filter(Otp.otp_id == otp_id).first()
        if db_otp:
            db_otp.attempts = attempts
            db.commit()
            db.refresh(db_otp)
            logger.info(f"OTP with ID {otp_id} updated successfully.")
            return db_otp
        else:
            logger.warning(f"OTP with ID {otp_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP not found")
    except Exception as e:
        logger.error(f"Error updating OTP with ID {otp_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def delete_otp(db: Session, otp_id: int):
    """
    Delete a specific OTP from the database.

    Args:
        db (Session): The database session.
        otp_id (int): The ID of the OTP to delete.

    Returns:
        Otp: The deleted OTP object, if found.

    Raises:
        HTTPException: If an error occurs during deletion.
    """
    try:
        db_otp = db.query(Otp).filter(Otp.otp_id == otp_id).first()
        if db_otp:
            db.delete(db_otp)
            db.commit()
            logger.info(f"OTP with ID {otp_id} deleted successfully.")
            return db_otp
        else:
            logger.warning(f"OTP with ID {otp_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP not found")
    except Exception as e:
        logger.error(f"Error deleting OTP with ID {otp_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def get_otps(db: Session) -> list[Otp]:
    """
    Retrieve all OTPs from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[Otp]: A list of all OTP objects.

    Raises:
        HTTPException: If an error occurs during retrieval.
    """
    try:
        otps = db.query(Otp).all()
        logger.info(f"Retrieved {len(otps)} OTPs from the database.")
        return otps
    except Exception as e:
        logger.error(f"Error retrieving OTPs: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
