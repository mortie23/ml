import pytest
from database.database import create_task, read_tasks, update_task, delete_task


def test_create_task(test_db):
    # Test creating a new task
    create_task("New test task", test_db)
    tasks = read_tasks(test_db)
    assert len(tasks) == 4  # 3 from fixture + 1 new
    assert any(task[1] == "New test task" for task in tasks)


def test_read_tasks(test_db):
    # Test reading tasks
    tasks = read_tasks(test_db)
    assert len(tasks) == 3
    assert all(isinstance(task[0], int) for task in tasks)
    assert all(isinstance(task[1], str) for task in tasks)


def test_update_task(test_db):
    # Test updating a task
    tasks = read_tasks(test_db)
    first_task_id = tasks[0][0]
    update_task(first_task_id, "Updated task", test_db)
    updated_tasks = read_tasks(test_db)
    assert any(task[1] == "Updated task" for task in updated_tasks)


def test_delete_task(test_db):
    # Test deleting a task
    tasks = read_tasks(test_db)
    initial_count = len(tasks)
    first_task_id = tasks[0][0]
    delete_task(first_task_id, test_db)
    remaining_tasks = read_tasks(test_db)
    assert len(remaining_tasks) == initial_count - 1
