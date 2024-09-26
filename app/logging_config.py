import logging
import logging.config
import sys
import os
from datetime import datetime

# Get current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Define the logs directory path
logs_dir = "logs"

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": sys.stdout,  # Output to console
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(logs_dir, f"api-log-{current_date}.log"),  # Log to a file with date
            "when": "midnight",  # Rotate at midnight
            "backupCount": 30,   # Keep 30 days of logs
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "fastapi": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

def setup_logging():
    # Ensure the logs directory exists
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Update the filename with the current date
    LOGGING_CONFIG['handlers']['file']['filename'] = os.path.join(logs_dir, f"api-log-{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")
