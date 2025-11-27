from queue_manager import QueueManager, QueueEmptyException
from utils import save_queue, load_queue

def main():
    queues = {"default": QueueManager()}  # all queues stored here
    current = "default"                   # active queue name

    print("Welcome to Queue Manager!")
    print("Commands: new <name>, use <name>, queues, enqueue <item>, dequeue, view, save, load, exit")

    while True:
        command = input(f"[{current}] > ").strip()

        # Exit program
        if command == "exit":
            print("Goodbye!")
            break

        # Create a new queue
        elif command.startswith("new "):
            name = command.split(" ", 1)[1].strip()
            if name in queues:
                print(f"Queue '{name}' already exists.")
            else:
                queues[name] = QueueManager()
                print(f"Queue '{name}' created.")

        # Switch active queue
        elif command.startswith("use "):
            name = command.split(" ", 1)[1].strip()
            if name not in queues:
                print(f"Queue '{name}' does not exist.")
            else:
                current = name
                print(f"Switched to queue '{name}'.")

        # List available queues
        elif command == "queues":
            print("Available queues:")
            for name in queues:
                marker = "(active)" if name == current else ""
                print(f" - {name} {marker}")

        # Enqueue
        elif command.startswith("enqueue "):
            item = command.split(" ", 1)[1].strip()
            queues[current].enqueue(item)

        # Dequeue
        elif command == "dequeue":
            try:
                queues[current].dequeue()
            except QueueEmptyException as e:
                print(e)

        # View queue
        elif command == "view":
            queues[current].view()

        # Save active queue
        elif command == "save":
            save_queue(queues[current].queue, filename=f"{current}.json")
            print(f"Queue '{current}' saved.")

        elif command == "save_all":
            for name, q in queues.items():
                save_queue(q.queue, filename=f"{name}.json")
            print("All queues saved.")

        # Load active queue
        elif command == "load":
            queues[current].queue = load_queue(filename=f"{current}.json")
            print(f"Queue '{current}' loaded.")

        # Unknown command
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
