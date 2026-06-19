from pawpal_system import Pet, Task


def test_add_task_increases_pet_task_count():
    pet = Pet("Rex", "dog", 3)

    # A new pet starts out with no tasks.
    assert len(pet.tasks) == 0

    pet.add_task(Task("Morning feeding", 10, "morning", 1, "feeding"))

    # Adding a task increases the pet's task count by one.
    assert len(pet.tasks) == 1


def test_mark_complete_changes_status():
    task = Task("Morning feeding", 10, "morning", 1, "feeding")

    # A new task starts out incomplete.
    assert task.is_complete is False

    task.mark_complete()

    # Calling mark_complete() flips the status to complete.
    assert task.is_complete is True

