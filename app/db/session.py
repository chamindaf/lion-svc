from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.config import DATABASE_URL
from app.db.base import Base
import logging

# Set up logging for session handling
logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine with logging enabled
engine = create_engine(DATABASE_URL, echo=True)

def test_connection():
    """
    Tests the database connection by executing a simple query.
    
    Raises:
    - SQLAlchemyError: If the connection to the database fails.
    
    Logs the success or failure of the database connection.
    """
    try:
        with engine.connect() as connection:
            logger.info("Database engine connection successful.")
    except SQLAlchemyError as e:
        logger.error(f"Database engine connection failed: {e}")
        raise

# Call test_connection to ensure the database is accessible
test_connection()

# Create a configured "Session" class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database and create tables if they do not exist.
    
    This function imports all models and attempts to create the necessary 
    database tables. Logs any errors encountered during the process.
    
    Raises:
    - SQLAlchemyError: If table creation fails.
    """
    try:
        from app.models import Lookup, User, Request  # Import models for table creation
        
        # Create tables based on models defined in Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

# Dependency for getting a new database session
def get_db():
    """
    Provides a database session that can be used in FastAPI endpoints.
    
    Ensures the session is properly closed after use. Yields the session 
    object to the calling context (FastAPI endpoints).
    
    Yields:
    - A new session from SessionLocal.
    
    Logs any errors related to session handling.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        logger.info("Database session closed.")
