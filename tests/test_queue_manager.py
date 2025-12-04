import pytest
from queue_manager.queue_manager import QueueManager
from queue_manager.queue_manager_exceptions import QueueEmptyException

def test_enqueue_and_view():
    q = QueueManager("test")
    q.enqueue("first")
    q.enqueue("second")

    # assert q.view() == ["first", "second"]

def test_dequeue():
    q = QueueManager("test")
    q.enqueue("item1")

    removed = q.dequeue()

    assert removed == "item1"
    # assert q.view() == []

def test_dequeue_empty_should_raise():
    q = QueueManager("test")

    with pytest.raises(QueueEmptyException):
        q.dequeue()
