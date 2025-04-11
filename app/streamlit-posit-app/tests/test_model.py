from database.model import Task


def test_task_creation():
    # Test task model instance creation
    task = Task(task="Test task")
    assert task.task == "Test task"
    assert task.id is None  # ID is set by database


def test_task_representation():
    # Test string representation
    task = Task(id=1, task="Test task")
    assert str(task) == "<Task(id=1, task='Test task')>"
