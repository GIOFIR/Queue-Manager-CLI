import logging
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "queue_manager.log")

# Create the logs directory if missing
os.makedirs(LOGS_DIR, exist_ok=True)

# Create rotating handler
handler = RotatingFileHandler(
    LOG_FILE,
    # maxBytes=1_000_000,   # 1 MB per file
    maxBytes=1_000,   # 1 MB per file
    backupCount=5,        # Keep last 5 logs
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
handler.setFormatter(formatter)

# Configure logging
logger = logging.getLogger("queue_manager")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

def clear_logs():
    """
    Delete all log files inside the LOGS_DIR folder.
    Handles missing folders, permission errors, locked files, etc.
    """
    # Check if the logs directory exists
    if not os.path.exists(LOGS_DIR):
        print("No logs to clear.")
        return

    removed = []     # Successfully deleted files
    failed = []      # Files that could not be deleted

    try:
        # Iterate over all files inside the logs directory
        for file in os.listdir(LOGS_DIR):
            path = os.path.join(LOGS_DIR, file)

            # Skip subfolders – we only delete files
            if not os.path.isfile(path):
                continue

            try:
                os.remove(path)          # Attempt to delete file
                removed.append(file)     # Track successful deletion
            except PermissionError:
                # File is locked or permission denied
                failed.append((file, "Permission denied"))
            except FileNotFoundError:
                # File disappeared between listing and deletion
                failed.append((file, "File not found"))
            except OSError as e:
                # Any other OS-level error (I/O, filesystem, etc.)
                failed.append((file, f"OS error: {e}"))

        # Summary output
        print(f"Cleared {len(removed)} log files.")
        if removed:
            print("Removed:", removed)

        if failed:
            print("\n⚠ Some files could not be deleted:")
            for name, reason in failed:
                print(f" - {name}: {reason}")

    except Exception as e:
        # A global fallback – should almost never happen
        print(f"Unexpected error during log cleanup: {e}")

def set_log_level(choise):
    """change the log level"""
    upper_choise = choise.upper()
    log_level_options = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if upper_choise not in log_level_options:
        print(f"The log level choise {upper_choise} is not valid")
        print(f"valid choises are: {log_level_options}")
        return
    logger.setLevel(upper_choise)
    logger.info(f"Log level altered to {upper_choise}")