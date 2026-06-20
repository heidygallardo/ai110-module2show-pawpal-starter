from datetime import date

from pawpal_system import Pet, Scheduler, Task


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


def test_sort_by_time_returns_chronological_order():
    # Tasks deliberately added out of chronological order, using the
    # zero-padded "HH:MM" 24-hour times that sort_by_time expects.
    evening = Task("Evening walk", 20, "18:30", 2, "exercise")
    morning = Task("Morning feeding", 10, "07:00", 1, "feeding")
    noon = Task("Midday meds", 5, "12:15", 1, "medical")
    scheduler = Scheduler([evening, morning, noon], availability=60)

    ordered = scheduler.sort_by_time(scheduler.tasks)

    # Tasks come back earliest-to-latest by time of day.
    assert [task.time for task in ordered] == ["07:00", "12:15", "18:30"]

    # Sorting does not mutate the scheduler's original task list.
    assert [task.time for task in scheduler.tasks] == ["18:30", "07:00", "12:15"]


def test_completing_daily_task_creates_task_for_next_day():
    pet = Pet("Rex", "dog", 3)
    task = Task(
        "Morning feeding",
        10,
        "morning",
        1,
        "feeding",
        recurrence="daily",
        due_date=date(2026, 6, 19),
    )
    pet.add_task(task)

    new_task = pet.complete_task(task)

    # The original task is marked complete.
    assert task.is_complete is True

    # A follow-up task was created for the next day...
    assert new_task is not None
    assert new_task.due_date == date(2026, 6, 20)
    # ...and it starts out incomplete.
    assert new_task.is_complete is False

    # The pet now holds both the completed task and tomorrow's occurrence.
    assert pet.tasks == [task, new_task]


def test_detect_conflicts_flags_duplicate_times():
    walk = Task("Evening walk", 20, "18:00", 2, "exercise")
    feeding = Task("Evening feeding", 10, "18:00", 1, "feeding")  # same time slot
    meds = Task("Midday meds", 5, "12:00", 1, "medical")  # no clash
    scheduler = Scheduler([walk, feeding, meds], availability=60)

    warnings = scheduler.detect_conflicts()

    # Exactly one slot is contested, so exactly one warning is raised.
    assert len(warnings) == 1
    # The warning names the contested time and both clashing tasks.
    assert "18:00" in warnings[0]
    assert "Evening walk" in warnings[0]
    assert "Evening feeding" in warnings[0]
    # The uncontested 12:00 task is not mentioned.
    assert "Midday meds" not in warnings[0]


def test_detect_conflicts_returns_empty_when_all_times_unique():
    tasks = [
        Task("Morning feeding", 10, "07:00", 1, "feeding"),
        Task("Midday meds", 5, "12:00", 1, "medical"),
        Task("Evening walk", 20, "18:00", 2, "exercise"),
    ]
    scheduler = Scheduler(tasks, availability=60)

    # No shared time slots means no conflict warnings.
    assert scheduler.detect_conflicts() == []

