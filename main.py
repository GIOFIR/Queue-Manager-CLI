from queue_manager import QueueManager, QueueEmptyException
from utils import save_queue, load_queue, queues_directory_exists, save_all_queues, show_all_queues, get_command, remove_from_index, print_queue

def main():  
      
    queues_directory_exists()

    print("Welcome to Queue Manager!")
    print("Commands: new <name>, add <name> <item>, save <name>, save-all, load <name>, show-all, show-queue <name>, delete<name>, exit")

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
                if command[1] == 'all':
                    save_all_queues(queues)
                    continue
                elif command[1] not in queues:
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
                    print(f"Queue '{command[1]}' loaded successfully.")

            case "show-all":
                show_all_queues()
            
            case "show-queue":
                queues[command[1]].view()
            
            case "delete":
                if queues.pop(command[1], "Not found") != "Not found":
                    remove_from_index(command[1])
                    print(f"Queue '{command[1]}' delted successfully.")
                else:
                    print(f"Could not delete the {command[1]} queue")

            case "exit":
                print("Goodbye!\n")
                break
            case _:  # Default case
                print(f"Unknown command: {" ".join(command)}")
                print("Commands: new <name>, add <name> <item>, save <name>, save-all, load <name>, show-all, show-queue <name>, delete<name>, exit")

if __name__ == "__main__":
    main()

