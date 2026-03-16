from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes — simple value-holding objects (Task, Pet)
# ---------------------------------------------------------------------------

@dataclass
class Task:
    name: str
    duration: int          # minutes
    priority: str          # "low" | "medium" | "high"
    category: str
    frequency: str = "once"   # "once" | "daily" | "weekly" | "monthly"
    completed: bool = False
    time: str = "08:00"       # scheduled start time in "HH:MM" format

    def update_priority(self, new_priority: str) -> None:
        """Set a new priority level for this task."""
        
        self.priority = new_priority

    def update_duration(self, new_duration: int) -> None:
        """Update how long this task takes in minutes."""

        self.duration = new_duration

    def update_frequency(self, new_frequency: str) -> None:
        """Update how often this task recurs."""

        self.frequency = new_frequency

    def mark_complete(self) -> None:
        """Mark this task as completed."""

        self.completed = True

    def get_task_info(self) -> dict:
        """Return all task attributes as a dictionary."""

        return {
            "name": self.name,
            "duration": self.duration,
            "priority": self.priority,
            "category": self.category,
            "frequency": self.frequency,
            "completed": self.completed,
        }


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet's task list."""

        self.tasks.append(task)

    def edit_task(self, task_name: str, **updates) -> None:
        """Update fields on the first task matching the given name."""

        for task in self.tasks:
            if task.name == task_name:
                for key, value in updates.items():
                    setattr(task, key, value)

    def remove_task(self, task_name: str) -> None:
        """Remove all tasks matching the given name."""

        self.tasks = [task for task in self.tasks if task.name != task_name]

    def get_tasks(self) -> list[Task]:
        """Return the full list of tasks for this pet."""

        return self.tasks


# ---------------------------------------------------------------------------
# Regular classes — objects with richer behavior (Owner, Scheduler)
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, availability: Optional[list] = None, preferences: Optional[dict] = None):
        self.name: str = name
        self.availability: list = availability or []
        self.preferences: dict = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""

        self.pets.append(pet)

    def edit_pet(self, pet_name: str, **updates) -> None:
        """Update fields on the first pet matching the given name."""

        for pet in self.pets:
            if pet.name == pet_name:
                for key, value in updates.items():
                    setattr(pet, key, value)

    def remove_pet(self, pet_name: str) -> None:
        """Remove all pets matching the given name."""

        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def view_pets(self) -> list[Pet]:
        """Return the full list of this owner's pets."""

        return self.pets

    def view_all_tasks(self) -> list[Task]:
        """Return a flat list of all tasks across every pet."""

        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    def __init__(self, tasks: Optional[list[Task]] = None, availability: Optional[list] = None):
        self.tasks: list[Task] = tasks or []
        self.availability: list = availability or []
        self.daily_plan: list[Task] = []
        self.explanation: str = ""

    def generate_plan(self) -> None:
        """Build the daily plan by sorting tasks and filtering by available time."""

        sorted_tasks = self.sort_tasks_by_priority()
        self.daily_plan = self.filter_tasks_by_time(sorted_tasks)
        self.explanation = self.build_explanation()

    @staticmethod
    def _to_minutes(time_str: str) -> int:
        """Convert a 'HH:MM' time string to total minutes since midnight.

        Used internally to turn start times into plain integers so that
        overlap arithmetic (start + duration) works without datetime objects.

        Args:
            time_str: A zero-padded time string, e.g. '08:30' or '14:00'.

        Returns:
            Integer total minutes since midnight, e.g. '08:30' -> 510.
        """

        h, m = (int(x) for x in time_str.split(":"))
        return h * 60 + m

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for any tasks whose time windows overlap.

        Two tasks conflict when one starts before the other has finished,
        regardless of whether they belong to the same pet or different pets.
        Returns an empty list if no conflicts are found.
        """

        warnings = []
        for i, a in enumerate(self.tasks):
            for b in self.tasks[i + 1:]:
                a_start = self._to_minutes(a.time)
                b_start = self._to_minutes(b.time)

                # get task end times
                a_end = a_start + a.duration
                b_end = b_start + b.duration

                # handle conflict
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"WARNING: '{a.name}' ({a.time}, {a.duration} min) "
                        f"conflicts with '{b.name}' ({b.time}, {b.duration} min)."
                    )

        return warnings

    def filter_tasks_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completion status.

        Pass completed=True to get finished tasks, False for pending ones.
        """

        return [t for t in self.tasks if t.completed == completed]

    def sort_tasks_by_time(self) -> list[Task]:
        """Return tasks sorted by scheduled start time (earliest first)."""

        return sorted(self.tasks, key=lambda t: tuple(int(x) for x in t.time.split(":")))

    def sort_tasks_by_priority(self) -> list[Task]:
        """Return tasks sorted from highest to lowest priority."""

        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda t: order.get(t.priority, 3))

    def filter_tasks_by_time(self, sorted_tasks: list[Task]) -> list[Task]:
        """Return tasks that fit within total available time, skipping completed ones."""

        total_available = sum(self.availability)
        plan, time_used = [], 0
        for task in sorted_tasks:
            if not task.completed and time_used + task.duration <= total_available:
                plan.append(task)
                time_used += task.duration
        return plan

    def build_explanation(self) -> str:
        """Generate explanation of why each task was chosen or skipped."""

        if not self.daily_plan:
            return "No tasks scheduled."

        total_available = sum(self.availability)
        total_used = sum(t.duration for t in self.daily_plan)
        skipped = [t for t in self.tasks if t not in self.daily_plan and not t.completed]

        lines = [f"- {t.name}: selected because it has {t.priority} priority ({t.duration} min)" for t in self.daily_plan]

        if skipped:
            skip_lines = [f"- {t.name}: skipped (not enough remaining time or lower priority)" for t in skipped]
            lines += ["\nSkipped:"] + skip_lines

        return (
            f"Plan uses {total_used} of {total_available} available minutes.\n"
            f"Tasks were sorted by priority (high → medium → low), then fit into available time:\n"
            + "\n".join(lines)
        )

    def get_plan(self) -> dict:
        """Return the daily plan and explanation as a dictionary."""

        return {"daily_plan": self.daily_plan, "explanation": self.explanation}
