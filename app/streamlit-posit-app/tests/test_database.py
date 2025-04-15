import pytest
from database.database import create_task, read_tasks, update_task, delete_task


def test_create_task(test_database_url):
    # Test creating a new task
    create_task("New test task", test_database_url)
    tasks = read_tasks(test_database_url)
    assert len(tasks) == 2
    assert any(task[1] == "New test task" for task in tasks)
    for task in tasks:
        new_task_id = task[0] if task[1] == "New test task" else 1
    delete_task(new_task_id, test_database_url)


def test_read_tasks(test_database_url):
    # Test reading tasks
    tasks = read_tasks(test_database_url)
    assert len(tasks) == 1
    assert all(isinstance(task[0], int) for task in tasks)
    assert all(isinstance(task[1], str) for task in tasks)


def test_update_task(test_database_url):
    # Test updating a task
    tasks = read_tasks(test_database_url)
    first_task_id = tasks[0][0]
    update_task(first_task_id, "Updated task", test_database_url)
    updated_tasks = read_tasks(test_database_url)
    assert any(task[1] == "Updated task" for task in updated_tasks)
    update_task(first_task_id, "seed", test_database_url)


def test_delete_task(test_database_url):
    # Test deleting a task
    create_task("New test task", test_database_url)
    tasks = read_tasks(test_database_url)
    initial_count = len(tasks)
    new_task_id = tasks[1][0]
    delete_task(new_task_id, test_database_url)
    remaining_tasks = read_tasks(test_database_url)
    assert len(remaining_tasks) == initial_count - 1
