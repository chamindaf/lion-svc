from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.password_security import hash_password, temp_password
import logging
from app.workflows.email import send_email
from app.config import OTP_TEST_EMAIL, OTP_TEST_CC_EMAIL, SEND_EMAIL_URL

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of users from the database.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        List[User]: A list of User objects.
    """
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(users)} users from the database.")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def update_user(db: Session, user_id: int, user_update: dict) -> User:
    """
    Update a user's information in the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        user_update (dict): Dictionary containing the fields to update.

    Returns:
        User: The updated User object.

    Raises:
        HTTPException: If the user with the given ID is not found.
    """
    try:
        # Convert dict to Pydantic model if necessary
        if not isinstance(user_update, UserUpdate):
            user_update = UserUpdate(**user_update)

        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            for key, value in user_update.model_dump(exclude_unset=True).items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User with ID {user_id} updated successfully.")
            return db_user
        else:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        logger.error(f"Error updating user with ID {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def create_user(db: Session, user_in: UserCreate, created_by: str) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user_in (UserCreate): The user data for the new user.
        created_by (str): Identifier of the user who created this record.

    Returns:
        User: The newly created User object.

    Raises:
        HTTPException: If the email is already registered.
    """
    try:
        temporary_password = temp_password()
        logger.info(f"Generating temporary password.")

        # Create a new User instance
        db_user = User(
            role=user_in.role,
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            vendor_id=user_in.vendor_id,
            company=user_in.company,
            contact=user_in.contact,
            hashed_password=hash_password(temporary_password),
            is_temp_password=True,
            is_active=False,
            created_by=created_by
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # Send the OTP to the user via email
        send_email(
            workflow_url=SEND_EMAIL_URL,
            email=user_in.email, 
            type="Temporary Password", 
            body= {
                    "Email": user_in.email,
                    "Firstname":user_in.first_name,
                    "Lastname":user_in.last_name,
                    "TempPassword": temporary_password 
                }
            )
        send_email(
            workflow_url=SEND_EMAIL_URL,
            email=OTP_TEST_EMAIL, 
            type="Temporary Password", 
            body={
                    "Email": OTP_TEST_EMAIL,
                    "TempPassword": temporary_password,
                    "Firstname":user_in.first_name,
                    "Lastname":user_in.last_name
                }
            )    # Only for testing purpose
        send_email(
            workflow_url=SEND_EMAIL_URL,
            email=OTP_TEST_CC_EMAIL, 
            type="Temporary Password", 
            body={
                    "Email": OTP_TEST_CC_EMAIL,
                    "TempPassword": temporary_password,
                    "Firstname":user_in.first_name,
                    "Lastname":user_in.last_name
                }
            ) # Only for testing purpose
        logger.info(f"User with ID {db_user.user_id} created successfully.")
        return db_user
    except IntegrityError:
        db.rollback()
        logger.error(f"Email {user_in.email} is already registered.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def reset_password(db: Session, db_user: User, new_password: str) -> User:
    """
    Reset the password for an existing user.

    Args:
        db (Session): The database session.
        db_user (User): The User object for which to reset the password.
        new_password (str): The new password to set.

    Returns:
        User: The updated User object.
    """
    try:
        db_user.hashed_password = hash_password(new_password)
        db_user.is_temp_password = False
        db.commit()
        db.refresh(db_user)
        logger.info(f"Password reset successfully for user with ID {db_user.user_id}.")
        return db_user
    except Exception as e:
        logger.error(f"Error resetting password for user with ID {db_user.user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user from the database by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.

    Returns:
        User: The user object if found, else None.
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            logger.info(f"User found with email: {email}")
        else:
            logger.info(f"No user found with email: {email}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user with email {email}: {e}")
        raise

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a user from the database by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.

    Returns:
        User: The user object if found, else None.
    """
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            logger.info(f"User found with id: {user_id}")
        else:
            logger.info(f"No user found with id: {user_id}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user with id {user_id}: {e}")
        raise
