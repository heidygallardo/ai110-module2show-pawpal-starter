"""PawPal+ system skeleton.

Class structure generated from diagrams/uml_draft.mmd.
Method bodies are left as stubs to be implemented.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity."""

    name: str
    duration: int  # minutes
    time: str
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
    preferences: dict = field(default_factory=dict)
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
    availability: str
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
    """Builds a daily care plan from a pet's tasks and time constraints."""

    def generate_plan(self, pet: Pet, available_time: int) -> list[Task]:
        """Produce a daily care plan for a pet within the available time."""
        pass

    def organize_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority."""
        pass

    def filter_to_constraints(self, tasks: list[Task], available_time: int) -> list[Task]:
        """Filter tasks so they fit within the available time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        pass
