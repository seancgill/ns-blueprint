# logging_setup.py
import logging
import os

def setup_logging():
    # Define the log file path in the 'logs' subdirectory
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)  # Create 'logs' directory if it doesn’t exist
    log_file = os.path.join(log_dir, 'netsapiens_api.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),  # Log to logs/netsapiens_api.log
            logging.StreamHandler()  # Log to terminal
        ]
    )
    return logging.getLogger(__name__)