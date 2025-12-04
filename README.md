# Queue Manager CLI

A Python-based command-line tool for managing multiple named queues, including
persistent storage, logging, and automated tests.  
The project includes a modular architecture, exception handling, and CI-ready structure.

---

## Features

- Create and manage multiple named queues.
- Add and remove items from queues.
- Automatic persistent storage in JSON files.
- Logging of all operations.
- Tests using pytest.
- Modular design suitable for extension.

---

## Project Structure

project/
│ main.py
│ autocomplete.py
│ logger.py
│ utils.py
│ queue_manager.py
│ requirements.txt
│ README.md
│ run_all_tests.py
│
├── queue_manager/
│ queue_manager.py
│ queue_manager_exceptions.py
│ init.py
│
├── tests/
│ test_queue_manager.py
│
├── logs/
│ queue_manager.log
│
└── all_queues/


---

## Installation

### 1. Clone the repository

git clone <repository-url>
cd Queue-Manager-CLI


### 2. Create virtual environment (recommended)

python -m venv venv


Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt


---

## Running the CLI

python main.py

The CLI supports commands such as:

- `new <queue-name>` — Create a new queue
- `add <queue-name> <item>` — Add an item to a queue
- `pop-item <queue-name> <item>` — Remove an item from the queue
- `show-queue <queue-name>` — Display queue content

(Your autocomplete.py file handles command completion.)

---

## Running Tests

Tests are located in the `tests/` directory.

Run all tests:
pytest -v

Or using the provided script:

python run_all_tests.py


---

## Logging

The system writes logs to:

logs/queue_manager.log

All operations (queue creation, add, pop, errors) are logged for debugging and auditing.

---

## Continuous Integration (Optional)

You can add GitHub Actions support by adding:

.github/workflows/Queue Manager CLI Tests.yml

---

## Future Improvements

- Docker image for easier deployment

---

## License

MIT License

