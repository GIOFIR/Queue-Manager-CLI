from collections import deque
from queue_manager_exceptions import QueueEmptyException
class QueueManager:
    def __init__(self, name):
        self.queue = deque()
        self.name = name

    def set_name(self, name):
        self.name = name

    def set_queue(self, queue):
        self.queue = queue

    def enqueue(self, item):
        self.queue.append(item)
        print(f"Added '{item}'  to queue '{self.name}'.")

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
    def __str__(self):
        return f"QueueManager(name={self.name}, items={list(self.queue)})"

