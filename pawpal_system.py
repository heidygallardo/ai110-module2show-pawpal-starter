"""PawPal+ system skeleton.

Class structure generated from diagrams/uml_draft.mmd.
Method bodies are left as stubs to be implemented.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity."""

    name: str
    duration: int  # minutes the task takes — drives scheduling
    time: str  # preferred time of day (label / soft preference, not a hard constraint)
    priority: int
    category: str
    is_complete: bool = False

    def update_details(self, details: dict) -> None:
        """Update one or more task details."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        pass


@dataclass
class Pet:
    """A pet and the tasks associated with caring for it."""

    name: str
    species: str
    age: int
    medical_conditions: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        pass

    def edit_task(self, task: Task) -> None:
        """Edit an existing task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        pass

    def view_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    phone_number: str
    availability: int  # total time available, in minutes
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def edit_pet(self, pet: Pet) -> None:
        """Edit an existing pet."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass

    def view_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        pass

    def view_all_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        pass


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
    ):
        self.tasks = tasks
        self.availability = availability  # total time available, in minutes
        self.preferences = preferences or {}
        self.plan: list[Task] = []
        self.explanation: str = ""

    def generate_plan(self) -> list[Task]:
        """Build the daily care plan from self.tasks within self.availability.

        Stores the result in self.plan and the reasoning in self.explanation.
        """
        pass

    def organize_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (highest priority first)."""
        pass

    def filter_to_constraints(self, tasks: list[Task]) -> list[Task]:
        """Drop completed tasks and trim by duration to fit self.availability.

        Tasks are included until their total duration reaches the available
        time budget; a task's `time` is not treated as a hard constraint.
        """
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        pass
