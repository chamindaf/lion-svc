from sqlalchemy.orm import Session
from app.models.sf_tables import TerritoryInfo, ChannelInfo, BrandInfo
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

def get_territory_by_territory(db: Session, territory: str) -> TerritoryInfo:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Request type to retrieve.

    Returns:
        Request_Type: The Request type object if found, else None.
    """
    try:
        territory = db.query(TerritoryInfo).filter(TerritoryInfo.territory == territory).first()
        if territory:
            logger.info(f"Territory found for: {territory}")
        else:
            logger.info(f"No territory found for: {territory}")
        return territory
    except Exception as e:
        logger.error(f"Error retrieving territory for {territory}: {e}")
        raise

def get_channel_by_channel(db: Session, channel: str) -> ChannelInfo:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Request type to retrieve.

    Returns:
        Request_Type: The Request type object if found, else None.
    """
    try:
        channel = db.query(ChannelInfo).filter(ChannelInfo.channel == channel).first()
        if channel:
            logger.info(f"Channel found for: {channel}")
        else:
            logger.info(f"No channel found for: {channel}")
        return channel
    except Exception as e:
        logger.error(f"Error retrieving channel for {channel}: {e}")
        raise

def get_brand_by_brand(db: Session, brand: str) -> BrandInfo:
    """
    Retrieve a Request type from the database by their request_type_id.

    Args:
        db (Session): The database session.
        request_type_id (int): The request_type_id of the Request type to retrieve.

    Returns:
        Request_Type: The Request type object if found, else None.
    """
    try:
        brand = db.query(BrandInfo).filter(BrandInfo.brand == brand).first()
        if brand:
            logger.info(f"Brand found for: {brand}")
        else:
            logger.info(f"No brand found for: {brand}")
        return brand
    except Exception as e:
        logger.error(f"Error retrieving brand for {brand}: {e}")
        raise