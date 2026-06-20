"""PawPal+ system skeleton.

Class structure generated from diagrams/uml_draft.mmd.
Method bodies are left as stubs to be implemented.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """A single pet care activity."""

    name: str
    duration: int  # minutes the task takes — drives scheduling
    time: str  # preferred time of day (label / soft preference, not a hard constraint)
    priority: int
    category: str
    is_complete: bool = False
    recurrence: str = "none"  # "none" | "daily" | "weekly"
    due_date: date | None = None  # when this occurrence is due

    def update_details(self, details: dict) -> None:
        """Update one or more task details from a {field: value} mapping.

        Raises ValueError if a key does not match a Task field.
        """
        allowed = {
            "name",
            "duration",
            "time",
            "priority",
            "category",
            "is_complete",
            "recurrence",
            "due_date",
        }
        for key, value in details.items():
            if key not in allowed:
                raise ValueError(f"Unknown task field: '{key}'")
            setattr(self, key, value)

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True

    def next_occurrence(self) -> "Task | None":
        """Return a fresh, incomplete copy of this task due on the next date.

        Returns None if the task does not recur (or has no due date). The new
        due date is computed with timedelta, so month/year/leap-year rollovers
        are handled correctly (e.g. Jan 31 + 1 day -> Feb 1).
        """
        steps = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        if self.recurrence not in steps or self.due_date is None:
            return None
        return Task(
            name=self.name,
            duration=self.duration,
            time=self.time,
            priority=self.priority,
            category=self.category,
            recurrence=self.recurrence,
            due_date=self.due_date + steps[self.recurrence],
        )


@dataclass
class Pet:
    """A pet and the tasks associated with caring for it."""

    name: str
    species: str
    age: int
    medical_conditions: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet.

        Raises ValueError if a task with the same name already exists.
        """
        if any(t.name == task.name for t in self.tasks):
            raise ValueError(f"A task named '{task.name}' already exists.")
        self.tasks.append(task)

    def edit_task(self, task: Task) -> None:
        """Replace the existing task that has the same name with `task`.

        Raises ValueError if no task with that name exists.
        """
        for i, existing in enumerate(self.tasks):
            if existing.name == task.name:
                self.tasks[i] = task
                return
        raise ValueError(f"No task named '{task.name}' found.")

    def remove_task(self, task: Task) -> None:
        """Remove the task with the matching name from this pet.

        Raises ValueError if no task with that name exists.
        """
        for i, existing in enumerate(self.tasks):
            if existing.name == task.name:
                del self.tasks[i]
                return
        raise ValueError(f"No task named '{task.name}' found.")

    def complete_task(self, task: Task) -> Task | None:
        """Mark `task` complete and add its next occurrence if it recurs.

        Returns the newly created task, or None if the task does not repeat.
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task

    def view_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return list(self.tasks)


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    phone_number: str
    availability: int  # total time available, in minutes
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner.

        Raises ValueError if a pet with the same name already exists.
        """
        if any(p.name == pet.name for p in self.pets):
            raise ValueError(f"A pet named '{pet.name}' already exists.")
        self.pets.append(pet)

    def edit_pet(self, pet: Pet) -> None:
        """Replace the existing pet that has the same name with `pet`.

        Raises ValueError if no pet with that name exists.
        """
        for i, existing in enumerate(self.pets):
            if existing.name == pet.name:
                self.pets[i] = pet
                return
        raise ValueError(f"No pet named '{pet.name}' found.")

    def remove_pet(self, pet: Pet) -> None:
        """Remove the pet with the matching name from this owner.

        Raises ValueError if no pet with that name exists.
        """
        for i, existing in enumerate(self.pets):
            if existing.name == pet.name:
                del self.pets[i]
                return
        raise ValueError(f"No pet named '{pet.name}' found.")

    def view_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return list(self.pets)

    def view_all_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Builds a daily care plan from tasks, availability, and constraints.

    The scheduler is configured with everything it needs up front, then
    `generate_plan()` produces and stores the plan so `explain_plan()` can
    describe it without extra arguments.
    """

    def __init__(
        self,
        tasks: list[Task],
        availability: int,
        preferences: dict | None = None,
        pet_by_task: dict[int, str] | None = None,
    ):
        self.tasks = tasks
        self.availability = availability  # total time available, in minutes
        self.preferences = preferences or {}
        # Maps id(task) -> pet name so the plan can show who each task is for.
        self.pet_by_task = pet_by_task or {}
        self.plan: list[Task] = []
        self.explanation: str = ""

    def generate_plan(self) -> list[Task]:
        """Build the daily care plan from self.tasks within self.availability.

        Orders tasks by priority, then includes them until the time budget is
        reached. Stores the result in self.plan and the reasoning in
        self.explanation, and returns the plan.
        """
        prioritized = self.organize_by_priority(self.tasks)
        self.plan = self.filter_to_constraints(prioritized)
        self.explanation = self.explain_plan()
        return self.plan

    def organize_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority (lower number = higher priority)."""
        return sorted(tasks, key=lambda task: task.priority)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by their 'HH:MM' time attribute.

        Zero-padded 24-hour times sort chronologically as plain strings,
        so the lambda keys directly on task.time.
        """
        return sorted(tasks, key=lambda task: task.time)

    def filter_by_pet(self, tasks: list[Task], pet_name: str) -> list[Task]:
        """Return only the tasks that belong to the pet named `pet_name`.

        Uses self.pet_by_task (id(task) -> pet name) to decide ownership,
        so each task must have been registered with the scheduler.
        """
        return [
            task for task in tasks if self.pet_by_task.get(id(task)) == pet_name
        ]

    def detect_conflicts(self, tasks: list[Task] | None = None) -> list[str]:
        """Return warning messages for tasks that share the same time slot.

        Lightweight: groups tasks by their `time` value; any slot holding more
        than one task is flagged (same pet or different pets). Returns an empty
        list when there are no conflicts and never raises, so callers can show
        warnings without interrupting scheduling.
        """
        tasks = self.tasks if tasks is None else tasks
        by_time: dict[str, list[Task]] = {}
        for task in tasks:
            by_time.setdefault(task.time, []).append(task)

        warnings: list[str] = []
        for time_slot, clashing in sorted(by_time.items()):
            if len(clashing) > 1:
                who = ", ".join(
                    f"{self.pet_by_task.get(id(t), '?')}'s {t.name}"
                    for t in clashing
                )
                warnings.append(f"[!] Conflict at {time_slot}: {who}")
        return warnings

    def filter_to_constraints(self, tasks: list[Task]) -> list[Task]:
        """Drop completed tasks and trim by duration to fit self.availability.

        Walks the (already prioritized) tasks and includes each one whose
        duration still fits the remaining time budget; a task's `time` is not
        treated as a hard constraint.
        """
        selected: list[Task] = []
        remaining = self.availability
        for task in tasks:
            if task.is_complete:
                continue
            if task.duration <= remaining:
                selected.append(task)
                remaining -= task.duration
        return selected

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan.

        Tasks are grouped under a heading for each time of day and shown in
        aligned columns: pet, task name, duration, priority, and category.
        """
        if not self.plan:
            return "No tasks could be scheduled within the available time."

        used = sum(task.duration for task in self.plan)
        # Widest pet/name across the plan, so columns line up regardless of data.
        pet_width = max(len(self.pet_by_task.get(id(t), "?")) for t in self.plan)
        name_width = max(len(t.name) for t in self.plan)

        header = (
            f"Scheduled {len(self.plan)} task(s) "
            f"using {used} of {self.availability} available minutes"
        )
        lines = [header, "=" * len(header)]

        # Keep tasks in plan order within a stable ordering of time-of-day groups.
        time_order = ["morning", "afternoon", "evening", "night"]
        groups = sorted(
            {task.time for task in self.plan},
            key=lambda t: (time_order.index(t) if t in time_order else len(time_order), t),
        )
        for time_of_day in groups:
            lines.append("")
            lines.append(f"{time_of_day.upper()}")
            for task in self.plan:
                if task.time != time_of_day:
                    continue
                pet = self.pet_by_task.get(id(task), "?")
                lines.append(
                    f"  • [{pet:<{pet_width}}] "
                    f"{task.name:<{name_width}}  "
                    f"{task.duration:>3} min  "
                    f"(priority {task.priority}, {task.category})"
                )
        return "\n".join(lines)
