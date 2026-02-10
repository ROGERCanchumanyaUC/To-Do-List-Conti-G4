import pytest

@pytest.fixture
def setup_task_manager():
    # Setup code to initialize the task manager
    task_manager = TaskManager()
    return task_manager


def test_add_task(setup_task_manager):
    task_manager = setup_task_manager
    task = task_manager.add_task("Task 1")
    assert task_manager.get_tasks() == [task]


def test_update_task(setup_task_manager):
    task_manager = setup_task_manager
    task = task_manager.add_task("Task 1")
    updated_task = task_manager.update_task(task.id, "Updated Task")
    assert updated_task.name == "Updated Task"


def test_delete_task(setup_task_manager):
    task_manager = setup_task_manager
    task = task_manager.add_task("Task 1")
    task_manager.delete_task(task.id)
    assert task_manager.get_tasks() == []


def test_get_nonexistent_task(setup_task_manager):
    task_manager = setup_task_manager
    with pytest.raises(TaskNotFoundException):
        task_manager.get_task(99)  # Assuming 99 is an invalid id


def test_add_task_edge_case(setup_task_manager):
    task_manager = setup_task_manager
    task = task_manager.add_task("")  # Edge case for empty task name
    assert task_manager.get_tasks() == [task]
    assert task.name == ""


def test_task_manager_maximum_capacity(setup_task_manager):
    task_manager = setup_task_manager
    # Assuming maximum capacity is 10 tasks
    for i in range(10):
        task_manager.add_task(f"Task {i + 1}")
    with pytest.raises(TaskManagerFullException):
        task_manager.add_task("Task 11")

# Add more tests as needed to cover all functionality and edge cases.
