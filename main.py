from queue_manager import QueueManager
from utils import *
from logger import clear_logs, set_log_level
from autocomplete import enable_autocomplete

def main():  

    enable_autocomplete()
    queues_directory_exists()
    print("Welcome to Queue Manager!")
    print_commands()
    queues = {}  # A dictionary: name → QueueManager()
    
    while True:
        command = get_command()
        match command[0].strip().lower():
            case "new":
                try:
                    queues[command[1]] = QueueManager(command[1])
                    print(f"The name of the new queue: {queues[command[1]].name}")
                except IndexError:
                    print(f"The correct form of the command is: new <name of the new queue>\n")
                    continue
                print(f"Queue '{command[1]}' created.")

            case "add":
                if command[1] not in queues:
                    print("Queue does not exist.")
                    continue
                queues[command[1]].enqueue(command[2])

            case "save":
                if command[1] not in queues:
                    print("Queue does not exist.")
                    continue
                save_queue(queues[command[1]], command[1])

            case "save-all":
                save_all_queues(queues)

            case "load":
                 temp_queue = load_queue(command[1])
                 if temp_queue is not None:
                    queues[command[1]] = QueueManager(command[1])
                    queues[command[1]].set_queue(temp_queue)
                    add_to_index(command[1])
                    print(f"Queue '{command[1]}' loaded successfully.")

            case "show-all":
                show_all_queues()
            
            case "show-queue":
                if command[1] not in queues:
                    print("Queue not found.")
                    continue
                queues[command[1]].view()
            
            case "set-log-level":
                set_log_level(command[1])

            case "delete":
                if command[1] in queues:
                    queues.pop(command[1])
                    delete_queue_file(command[1])
                    remove_from_index(command[1])
                    print(f"Queue '{command[1]}' deleted successfully.")
                else:
                    print(f"Queue '{command[1]}' not found.")
            
            case "clear-logs":
                clear_logs()

            case "exit":
                print("Goodbye!\n")
                break
            case _:  # Default case
                print(f"Unknown command: {''.join(command[1:])}")
                print_commands()

if __name__ == "__main__":
    main()

