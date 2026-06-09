"""
Logging utility for Weather Forecasting Application
"""
import logging
import sys
from pathlib import Path
from config.config import LOG_LEVEL, LOG_FORMAT, LOG_FILE, LOGS_DIR

def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Setup and return a configured logger
    
    Args:
        name: Logger name (typically __name__ of the module)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        LOGS_DIR.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not create file handler: {e}")
    
    return logger

def log_execution_time(logger: logging.Logger):
    """Decorator to log function execution time"""
    def decorator(func):
        import time
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        return wrapper
    return decorator
