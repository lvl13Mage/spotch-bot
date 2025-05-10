import logging
from logging.handlers import RotatingFileHandler
from backend.modules.logging.filters.sensitive_data_filter import SensitiveDataFilter
import os

def setup_logging():
    """Set up logging with file rotation and sensitive data filtering."""
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Create a rotating file handler for app logs
    app_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)

    # Create a rotating file handler for error logs
    error_handler = RotatingFileHandler(
        "logs/error.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Add the sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    app_handler.addFilter(sensitive_filter)
    error_handler.addFilter(sensitive_filter)

    # Add handlers to the logger
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)

    # Add a console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(sensitive_filter)  # Add the filter to the console handler
    logger.addHandler(console_handler)

    # Explicitly add the filter to uvicorn loggers
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addFilter(sensitive_filter)

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.addFilter(sensitive_filter)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.addFilter(sensitive_filter)