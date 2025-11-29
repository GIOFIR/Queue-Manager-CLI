class QueueEmptyException(Exception):
    """Exception raised when trying to dequeue from an empty queue."""
    pass
class QueueStorageInitException(Exception):
    """Raised when queue storage directory cannot be created."""
    pass
