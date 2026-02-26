import logging
import os

os.makedirs("logs", exist_ok=True)

def get_logger():

    logger = logging.getLogger("pipeline_logger")

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:

        file_handler = logging.FileHandler("logs/pipeline.log")

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger