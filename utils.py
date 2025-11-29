import json
import os
from collections import deque
from queue_manager_exceptions import QueueStorageInitException

# ----------------------------
# CONSTANTS
# ----------------------------
# Get absolute path to the project directory (folder where utils.py is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# where all queues stored
QUEUES_DIR = os.path.join(BASE_DIR, "all_queues")
# a list of all existing queues
INDEX_FILE = os.path.join(BASE_DIR, "queues_index.json")

def get_command():
    """receive a command from the user and return it as a list"""
    return input("\nCommand: ").split(" ")    

def queues_directory_exists():
    # Ensure the queues directory exists
    try:
        os.makedirs(QUEUES_DIR, exist_ok=True)
    except PermissionError:
        raise QueueStorageInitException("No permission to create queue storage directory.")
    except FileNotFoundError:
        raise QueueStorageInitException("Invalid directory path for queue storage.")
    except OSError as e:
        raise QueueStorageInitException(f"Failed to initialize queue storage: {e}")


# ----------------------------
# SAVE / LOAD QUEUE
# ----------------------------
def save_queue(queue, name):
    """Save a single queue to a file."""
    file_path = os.path.join(QUEUES_DIR, f"{name}.json")
    with open(file_path, "w") as f:
        json.dump(list(queue.queue), f, indent=4)

    add_to_index(name)
    print(f"Queue '{name}' saved successfully.")

def load_queue(name):
    """Load a queue from file by name."""
    file_path = os.path.join(QUEUES_DIR, f"{name}.json")
    if not os.path.exists(file_path):
        print(f"No queue named '{name}' found.")
        return None

    with open(file_path, "r") as f:
        items = json.load(f)
    
    add_to_index(name)

    return deque(items)

# ----------------------------
# SAVE ALL QUEUES
# ----------------------------
def save_all_queues(queue_dict):
    for name, queue in queue_dict.items():
        save_queue(queue, name)
    print("All queues saved.")

# ----------------------------
# INDEX FILE HELPERS
# ----------------------------
def load_index():
    """Load list of saved queue names."""
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r") as f:
        return json.load(f)

def save_index(queue_names):
    """Save updated queue name list."""
    with open(INDEX_FILE, "w") as f:
        json.dump(queue_names, f, indent=4)

def add_to_index(name):
    index = load_index()
    if name not in index:
        index.append(name)
        save_index(index)

def remove_from_index(name):
    index = load_index()
    if name in index:
        index.remove(name)
        save_index(index)

# ----------------------------
# SHOW ALL EXISTING QUEUES
# ----------------------------
def show_all_queues():
    index = load_index()
    if not index:
        print("No saved queues found.")
    else:
        print("Existing saved queues:")
        for name in index:
            print(f" - {name}")

def print_queue(queue):
    print(f"The {queue.name} queue:")
    queue.view()