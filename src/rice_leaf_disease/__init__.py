import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s : %(module)s : %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, 'running_logs.log')

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Ensure that running_logs.log is not a directory (in case it exists)
if os.path.isdir(log_filepath):
    raise IsADirectoryError(f"{log_filepath} is a directory, not a file.")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),  # Save the logs in the specified file path
        logging.StreamHandler(sys.stdout)    # Also print logs to the console
    ]
)

logger = logging.getLogger('rice_leaf_disease')
