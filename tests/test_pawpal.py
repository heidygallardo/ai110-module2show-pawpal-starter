from pawpal_system import Task, Pet, Owner, Scheduler

# Chronological Sort: Verify that sort_tasks_by_time() returns tasks in earliest-first order.
def test_sort_tasks_by_time_returns_chronological_order():
    # Arrange
    tasks = [
        Task(name="Evening Walk",  duration=30, priority="low",    category="exercise", time="18:00"),
        Task(name="Morning Feed",  duration=10, priority="high",   category="feeding",  time="07:30"),
        Task(name="Afternoon Nap", duration=60, priority="medium", category="rest",     time="13:00"),
    ]
    scheduler = Scheduler(tasks=tasks)

    # Act
    result = scheduler.sort_tasks_by_time()

    # Assert
    assert [t.time for t in result] == ["07:30", "13:00", "18:00"]


# Filter by Status: Verify that only incomplete tasks are returned when filtering for pending.
def test_filter_by_status_returns_only_incomplete_tasks():
    # Arrange
    done = Task(name="Morning Feed", duration=10, priority="high", category="feeding", time="07:30")
    done.mark_complete()
    pending1 = Task(name="Evening Walk",  duration=30, priority="low",    category="exercise", time="18:00")
    pending2 = Task(name="Afternoon Nap", duration=60, priority="medium", category="rest",     time="13:00")
    scheduler = Scheduler(tasks=[done, pending1, pending2])

    # Act
    result = scheduler.filter_tasks_by_status(completed=False)

    # Assert
    assert len(result) == 2
    assert all(not t.completed for t in result)
    assert done not in result


# Conflict Detection: Verify that tasks with overlapping time windows are flagged.
def test_detect_conflicts_flags_duplicate_times():
    # Arrange — both tasks start at 09:00, so they fully overlap
    task_a = Task(name="Morning Walk", duration=30, priority="high",   category="exercise", time="09:00")
    task_b = Task(name="Morning Feed", duration=15, priority="medium", category="feeding",  time="09:00")
    scheduler = Scheduler(tasks=[task_a, task_b])

    # Act
    warnings = scheduler.detect_conflicts()

    # Assert
    assert len(warnings) == 1
    assert "Morning Walk" in warnings[0]
    assert "Morning Feed" in warnings[0]


# Task Completion: Verify that calling mark_complete() actually changes the task's status.
def test_mark_complete_changes_status():
    task = Task(name="Bath", duration=30, priority="high", category="grooming")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True

# Task Addition: Verify that adding a task to a Pet increases that pet's task count.
def test_add_task_increases_count():
    pet = Pet(name="Ares", species="Dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Bath", duration=30, priority="high", category="grooming"))
    assert len(pet.get_tasks()) == 1

