# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The newly added features are as follows:

### `sort_tasks_by_time()`
Sorts all tasks by their scheduled start time, earliest first. Each task's `time` field (`"HH:MM"`) is converted into an `(hour, minute)` tuple so times compare chronologically, not as plain strings.

```python
scheduler.sort_tasks_by_time()
# → [Morning Walk 07:00, Litter Box 07:10, Brushing 10:00, ...]
```

### `filter_tasks_by_status(completed: bool)`
Returns only the tasks that match the given completion state — pending or done. Useful for showing what still needs to be done vs. what has already been completed today.

```python
scheduler.filter_tasks_by_status(completed=False)  # pending tasks
scheduler.filter_tasks_by_status(completed=True)   # finished tasks
```

### `detect_conflicts()`
Checks every unique pair of tasks for overlapping time windows using the interval overlap formula:

```
conflict  when  A.start < B.end  AND  B.start < A.end
```

Returns a list of warning strings — one per conflicting pair. Returns an empty list if the schedule is clean. Works across tasks from the same pet or different pets.

```python
for msg in scheduler.detect_conflicts():
    print(msg)
# WARNING: 'Morning Walk' (07:00, 20 min) conflicts with 'Litter Box' (07:10, 10 min).
```

A private helper `_to_minutes(time_str)` converts `"HH:MM"` to total minutes since midnight so that start/end arithmetic stays simple integer math.

## Testing PawPal+

```bash
python -m pytest tests/test_pawpal.py -v
```
The test suite covers:

- Task state — mark_complete() correctly flips a task's status from incomplete to complete
- Pet task management — adding a task to a Pet increases its task count
- Chronological sorting — sort_tasks_by_time() returns tasks ordered earliest to latest regardless of insertion order
- Status filtering — filter_tasks_by_status(completed=False) returns only pending tasks and excludes completed ones
- Conflict detection — detect_conflicts() flags two tasks that share the same start time as a scheduling conflict

My confidence Level in the system's reliability is 2 stars out of 5,
since I need to add more tests.