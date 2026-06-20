from datetime import date

from pawpal_system import Pet, Owner, Task, Scheduler

# Create an Owner 
mary = Owner('Mary', '8882151', 120)

# Create two pets
whiskers = Pet('Whiskers', 'cat', 3)
rex = Pet('Rex', 'dog', 5)

mary.add_pet(whiskers)
mary.add_pet(rex)

# Add three Tasks with different times to those pets
whiskers.add_task(Task('Morning feeding', 10, 'morning', 1, 'feeding'))
rex.add_task(Task('Afternoon walk', 30, 'afternoon', 2, 'exercise'))
rex.add_task(Task('Evening feeding', 15, 'evening', 1, 'feeding'))

# Map each task back to the pet it belongs to (keyed by task identity).
pet_by_task = {id(task): pet.name for pet in mary.pets for task in pet.tasks}

# Print "Today's Schedule"
print(f"            Today's Schedule for {mary.name}        ")
print("=====================================================")
scheduler = Scheduler(
    mary.view_all_tasks(),
    mary.availability,
    mary.preferences,
    pet_by_task=pet_by_task,
)
scheduler.generate_plan()
print(scheduler.explanation)

# --- Test: sort tasks by their "HH:MM" time attribute --------------------
# sort_by_time() keys on task.time, and zero-padded 24-hour strings sort
# chronologically as plain strings ("08:00" < "14:00" < "18:00").
time_tasks = [
    Task('Evening feeding', 15, '18:00', 1, 'feeding'),
    Task('Morning feeding', 10, '08:00', 1, 'feeding'),
    Task('Afternoon walk', 30, '14:00', 2, 'exercise'),
]

print("\nTasks before sorting by time:")
for task in time_tasks:
    print(f"  {task.time}  {task.name}")

sorted_by_time = scheduler.sort_by_time(time_tasks)

print("\nTasks after sort_by_time():")
for task in sorted_by_time:
    print(f"  {task.time}  {task.name}")

# --- Test: filter tasks by pet name -------------------------------------
# filter_by_pet() uses the scheduler's pet_by_task map to keep only the
# tasks that belong to the named pet.
for pet in mary.pets:
    pet_tasks = scheduler.filter_by_pet(scheduler.tasks, pet.name)
    print(f"\nTasks for {pet.name}:")
    for task in pet_tasks:
        print(f"  {task.time}  {task.name}")

# --- Test: recurring task auto-creates its next occurrence --------------
# Completing a daily/weekly task adds a fresh instance for the next date.
daily_meds = Task('Insulin shot', 5, '08:00', 1, 'medical',
                  recurrence='daily', due_date=date(2026, 1, 31))
whiskers.add_task(daily_meds)

print(f"\nBefore completing: {daily_meds.name} due {daily_meds.due_date}, "
      f"complete={daily_meds.is_complete}")

new_task = whiskers.complete_task(daily_meds)

print(f"After completing:  {daily_meds.name} complete={daily_meds.is_complete}")
print(f"Auto-created next: {new_task.name} due {new_task.due_date} "
      f"(daily: Jan 31 + 1 day rolls into February)")

# --- Test: detect scheduling conflicts ----------------------------------
# Build a small set where Whiskers and Rex are both booked at 08:00 (an
# owner can only be in one place at once), plus a clash-free 17:00 task.
conflict_tasks = [
    Task('Morning feeding', 10, '08:00', 1, 'feeding'),   # Whiskers
    Task('Morning walk', 20, '08:00', 2, 'exercise'),     # Rex  -> clashes
    Task('Evening play', 15, '17:00', 3, 'play'),         # Rex  -> no clash
]
conflict_pet_by_task = {
    id(conflict_tasks[0]): 'Whiskers',
    id(conflict_tasks[1]): 'Rex',
    id(conflict_tasks[2]): 'Rex',
}
conflict_scheduler = Scheduler(
    conflict_tasks, mary.availability, pet_by_task=conflict_pet_by_task
)

print("\nConflict check:")
conflicts = conflict_scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

