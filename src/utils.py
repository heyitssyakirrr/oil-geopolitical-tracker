import logging
import os
import sys
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger that writes to both console and a log file.
    Use this at the top of every module:
        logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger # avoid adding duplicate handlers
    
    formatter = logging.Formatter(
        # timestamp | log level (ERROR / INFO) | module name | message written
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler - prints to terminal
    console = logging.StreamHandler(sys.stdout) # print to terminal
    console.setFormatter(formatter)
    logger.addHandler(console) # add console handler to logger

    # File handler - writes to logs/ folder
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger