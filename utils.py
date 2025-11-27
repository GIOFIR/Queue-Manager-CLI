import json
import os
from collections import deque

# Get absolute path to the project directory (folder where utils.py is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_queue(q, filename="queue.json"):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(list(q), f)

def load_queue(filename="queue.json"):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "r") as f:
        items = json.load(f)
        return deque(items)
