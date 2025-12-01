import json
import os
from collections import deque
from logger import logger
from queue_manager_exceptions import QueueStorageInitException

# ----------------------------
# CONSTANTS
# ----------------------------
# Absolute path to the project directory (folder where utils.py is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# where all queues stored
QUEUES_DIR = os.path.join(BASE_DIR, "all_queues")
# a list of all existing queues
INDEX_FILE = os.path.join(BASE_DIR, "queues_index.json")

def print_commands():
    """prints the avalable commands to the stream"""
    print("Commands:")
    print("  new <name>            - Create a new queue with the given name")
    print("  add <name> <item>     - Add an item to the specified queue")
    print("  save <name>           - Save the specified queue to a file")
    print("  save-all              - Save all queues")
    print("  load <name>           - Load a queue from a file")
    print("  show-all              - Display all queues")
    print("  show-queue <name>     - Display the contents of a specific queue")
    print("  delete <name>         - Delete the specified queue")
    print("  set-log-level <level> - set the logs level of information")
    print("  clear-logs            - delete all logs in the logs directory")
    print("  exit                  - Exit the program")

def get_command():
    """
    Receives a command from the user, validates its structure,
    and returns it as a list.
    If invalid, returns ["===", "<error message>"].
    """
    command = input("\nCommand: ").strip()
    logger.info(f"Received command: {command}")

    if not command:
        return ["===", "Empty command"]

    parts = command.split()
    cmd = parts[0]

    # === Commands that expect exactly 1 argument ===
    one_arg_cmds = {"new", "save", "load", "show-queue", "set-log-level", "delete"}
    # === Commands that expect no arguments ===
    zero_arg_cmds = {"save-all", "show-all", "clear-logs", "exit"}

    # Special case: add <name> <item...>
    if cmd == "add":
        if len(parts) < 3:
            return ["===", "Usage: add <name> <item>"]
        # allow multi-word item
        name = parts[1]
        item = " ".join(parts[2:])
        return ["add", name, item]

    # Handle commands that require exactly one argument
    if cmd in one_arg_cmds:
        if len(parts) != 2:
            return ["===", f"Usage: {cmd} <name>"]
        return parts

    # Handle commands with zero arguments
    if cmd in zero_arg_cmds:
        if len(parts) != 1:
            return ["===", f"Usage: {cmd}"]
        return parts

    # Unknown command
    return ["==="] + parts

# def get_command():
#     """receive a command from the user and return it as a list"""
#     command = input("\nCommand: ")
#     logger.info(f"Received command: {command}")
#     parts = command.split()
#     if len(parts) >= 3 and parts[0] == "add":
#         return [parts[0], parts[1], " ".join(parts[2:])]
#     return parts

def queues_directory_exists():
    # Ensure the queues directory exists
    try:
        os.makedirs(QUEUES_DIR, exist_ok=True)
    except PermissionError:
        raise QueueStorageInitException("No permission to create queue storage directory.")
        logger.error(f"No permission to create queue storage directory: {e}")
    except FileNotFoundError:
        raise QueueStorageInitException("Invalid directory path for queue storage.")
        logger.error(f"Invalid directory path for queue storage: {e}")
    except OSError as e:
        raise QueueStorageInitException(f"Failed to initialize queue storage: {e}")
        logger.error(f"Failed to initialize queue storage: {e}")


# ----------------------------
# SAVE / LOAD QUEUE
# ----------------------------
def save_queue(queue, name):
    """Save a single queue to a file."""
    try:
        file_path = os.path.join(QUEUES_DIR, f"{name}.json")
        with open(file_path, "w") as f:
            json.dump(list(queue.queue), f, indent=4)
        add_to_index(name)
        print(f"Queue '{name}' saved successfully.")
        logger.info(f"Saved queue '{name}'.")
    except Exception as e:
        logger.error(f"Failed to save queue '{name}': {e}")
        raise

    
def load_queue(name):
    """Load a queue from file by name."""
    try:
        file_path = os.path.join(QUEUES_DIR, f"{name}.json")
        if not os.path.exists(file_path):
            print(f"No queue named '{name}' found.")
            return None

        with open(file_path, "r") as f:
            items = json.load(f)
        
        return deque(items)
    except FileNotFoundError:
        logger.warning(f"Attempted to load non-existent queue '{name}'.")
        raise
    except Exception as e:
        logger.error(f"Failed to load queue '{name}': {e}")
        raise

# ----------------------------
# SAVE ALL QUEUES
# ----------------------------
def save_all_queues(queue_dict):
    """Save all queues to files."""
    try:
        for name, queue in queue_dict.items():
            save_queue(queue, name)
        print("All queues saved.")
        logger.info(f"All queues saved.")
    except Exception as e:
        logger.error(f"Failed to save queue '{name}': {e}")
        raise

# ----------------------------
# DELETE QUEUE
# ----------------------------
def delete_queue_file(name):
    """Delete a file of queue."""
    try:
        file_path = os.path.join(QUEUES_DIR, f"{name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
        logger.info(f"Deleted queue '{name}'.")
    except Exception as e:
        logger.error(f"Failed to delete queue '{name}': {e}")
        raise

# ----------------------------
# INDEX FILE HELPERS
# ----------------------------
def load_index():
    """Load list of saved queue names."""
    try:
        if not os.path.exists(INDEX_FILE):
            return []
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Attempted to load non-existent file.")
        raise
    except Exception as e:
        logger.error(f"Failed to load index file: {e}")
        raise

def save_index(queue_names):
    """Save updated queue name list."""
    try:
        with open(INDEX_FILE, "w") as f:
            json.dump(queue_names, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save queue index file: {e}")
        raise

def add_to_index(name):
    """Add file name to index"""
    index = load_index()
    if name not in index:
        index.append(name)
        save_index(index)

def remove_from_index(name):
    """Remove file name from index"""
    index = load_index()
    if name in index:
        index.remove(name)
        save_index(index)

# ----------------------------
# SHOW ALL EXISTING QUEUES
# ----------------------------
def show_all_queues():
    """Prints all queues in index"""
    index = load_index()
    if not index:
        print("No saved queues found.")
    else:
        print("Existing saved queues:")
        for name in index:
            print(f" - {name}")
