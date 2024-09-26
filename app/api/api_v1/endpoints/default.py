from fastapi import APIRouter,  HTTPException, status
from app.schemas.default import AppInfo
import logging

router = APIRouter()

# Set up logging for this module
logger = logging.getLogger(__name__)

@router.get("/", response_model=AppInfo)
def get_app_info():
    """
    Provides information about the Lion Brewery (Ceylon) PLC Outlet System API, including its purpose, authentication method, and error codes.

    Returns:
        AppInfo: Detailed information about the API.
    """
    try:
        app_info = {
            "application_name": "Lion Brewery (Ceylon) PLC Outlet System",
            "version": "1.0.0",
            "description": (
                "This FastAPI-based Python application serves as the backend for the Lion Brewery (Ceylon) PLC Outlet System, "
                "enabling seamless management of outlet data. It offers a set of CRUD (Create, Read, Update, Delete) operations "
                "that interact with an MS SQL database to handle essential tasks related to brewery outlets. The API allows users "
                "to perform a range of operations, including but not limited to adding new outlets, retrieving outlet details, "
                "updating information, and managing users, ensuring efficient and secure data management."
            )
        }
        return AppInfo(**app_info)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")