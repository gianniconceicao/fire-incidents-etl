"""
This script is used to retrieve external parameters used in main.py.
As well as initializing correctly the logging function.
"""

import os
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler

# Load environment variables
log_directory = os.getenv("LOG_DIR", "./logs")
log_level = os.getenv("LOG_LEVEL", "INFO")

# Ensure the log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


def setup_logging():
    """
    Setup logging configuration with rotation based on the day.
    """
    log_filename = os.path.join(log_directory, "app.log")

    # Create new file when day changes
    log_handler = TimedRotatingFileHandler(
        log_filename,
        when="midnight",
        interval=1
    )

    log_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            log_handler,
            logging.StreamHandler()
        ]
    )


def get_script_arguments():
    """
    Parse script arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        '-if',
        required=True,
        # default="input/Fire_Incidents_20250505.csv", # Added to facilitate trying the code
        help='Input CSV file path.'
    )
    parser.add_argument(
        '--ingestion-date',
        '-id',
        required=False,
        # default="2025/01/01", # Added to facilitate trying the code
        help="Date of data to be ingested in 'yyyy/MM/dd' format, if null the entire file will be ingested."
    )

    return vars(parser.parse_args())
