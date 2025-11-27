from collections import deque
from queue_manager_exceptions import QueueEmptyException
class QueueManager:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)
        print(f"Added '{item}' to the queue.")

    def dequeue(self):
        if not self.queue:
            raise QueueEmptyException("Cannot dequeue from an empty queue!")
        item = self.queue.popleft()
        print(f"Removed '{item}' from the queue.")
        return item

    def view(self):
        if not self.queue:
            print("The queue is empty.")
        else:
            print("Queue contents:")
            for idx, item in enumerate(self.queue, start=1):
                print(f"{idx}. {item}")
