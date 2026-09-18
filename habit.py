"""
habit.py - Core Data Models (OOP & Encapsulation Showcase)

Module Map:
- Module 6: Type Conversion (ISO date strings <-> date objects)
- Module 7: Core Data Structures (set for history, dict for serialization)
- Module 8: Control Flow Statements (input validation, conditionals)
- Module 12: Object Oriented Programming (Encapsulation, Inheritance, Polymorphism)
"""

from datetime import date
from typing import Set, Dict, Any, Optional


class Habit:
    """
    Base class representing a general Habit.
    Demonstrates OOP concepts: encapsulation, properties, validation, and serialization.
    """

    def __init__(self, name: str, category: str = "General", created_date: Optional[str] = None):
        self.name = name  # Uses property setter for validation
        self.category = category
        self._created_date = created_date or date.today().isoformat()
        self._history: Set[str] = set()

    @property
    def name(self) -> str:
        """Getter for habit name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setter for habit name with validation (non-empty string required)."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Habit name must be a non-empty string.")
        self._name = value.strip()

    @property
    def category(self) -> str:
        """Getter for category."""
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        """Setter for category."""
        self._category = value.strip() if isinstance(value, str) and value.strip() else "General"

    @property
    def created_date(self) -> str:
        """Returns the ISO formatted date string when the habit was created."""
        return self._created_date

    @property
    def history(self) -> Set[str]:
        """Encapsulation: returns a copy of the history set to prevent external mutation."""
        return set(self._history)

    def mark_done(self, target_date: Optional[str] = None) -> bool:
        """
        Marks the habit as done for the given ISO date string (defaults to today).
        Returns True if marked as completed.
        """
        day_str = target_date or date.today().isoformat()
        self._history.add(day_str)
        return True

    def unmark_done(self, target_date: Optional[str] = None) -> bool:
        """Removes the habit completion for the given date."""
        day_str = target_date or date.today().isoformat()
        if day_str in self._history:
            self._history.remove(day_str)
            return True
        return False

    def is_done_today(self) -> bool:
        """Checks if the habit is marked done today."""
        return date.today().isoformat() in self._history

    def is_done_on(self, day_str: str) -> bool:
        """Checks if the habit is marked done on a specific ISO date."""
        return day_str in self._history

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the habit instance to a JSON-compatible dictionary."""
        return {
            "type": "base",
            "name": self._name,
            "category": self._category,
            "created_date": self._created_date,
            "history": sorted(list(self._history)),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Habit":
        """Factory method to construct Habit or appropriate subclass from dictionary."""
        habit_type = data.get("type", "boolean")
        if habit_type == "countable":
            return CountableHabit.from_dict(data)
        elif habit_type == "boolean":
            return BooleanHabit.from_dict(data)

        # Fallback base habit
        habit = cls(data["name"], data.get("category", "General"), data.get("created_date"))
        habit._history = set(data.get("history", []))
        return habit

    def __str__(self) -> str:
        return f"[{self.category}] {self.name} - Completed {len(self._history)} times"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', category='{self.category}')>"


class BooleanHabit(Habit):
    """
    Subclass representing simple binary done/not-done habits (e.g. Meditate, Journaling).
    Demonstrates inheritance and polymorphism.
    """

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "boolean"
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BooleanHabit":
        habit = cls(data["name"], data.get("category", "General"), data.get("created_date"))
        habit._history = set(data.get("history", []))
        return habit


class CountableHabit(Habit):
    """
    Subclass representing habits that require reaching a numerical target per day.
    (e.g., Drink 8 glasses of water, 50 pushups).
    Demonstrates method overriding, custom state, and target completion checks.
    """

    def __init__(
        self,
        name: str,
        category: str = "General",
        target: int = 1,
        unit: str = "times",
        created_date: Optional[str] = None,
    ):
        super().__init__(name, category, created_date)
        self.target = target
        self.unit = unit
        # Map: "YYYY-MM-DD" -> current count
        self._daily_counts: Dict[str, int] = {}

    @property
    def target(self) -> int:
        return self._target

    @target.setter
    def target(self, val: int) -> None:
        if not isinstance(val, int) or val <= 0:
            raise ValueError("Target must be a positive integer.")
        self._target = val

    @property
    def daily_counts(self) -> Dict[str, int]:
        return dict(self._daily_counts)

    def get_count(self, target_date: Optional[str] = None) -> int:
        day_str = target_date or date.today().isoformat()
        return self._daily_counts.get(day_str, 0)

    def record_progress(self, amount: int = 1, target_date: Optional[str] = None) -> bool:
        """
        Increments the progress for the day.
        If the target is reached, automatically marks the day as done.
        """
        day_str = target_date or date.today().isoformat()
        current = self._daily_counts.get(day_str, 0) + amount
        self._daily_counts[day_str] = current

        if current >= self._target:
            self._history.add(day_str)
            return True
        return False

    def mark_done(self, target_date: Optional[str] = None) -> bool:
        """Marks habit complete by setting count directly to target if needed."""
        day_str = target_date or date.today().isoformat()
        self._daily_counts[day_str] = max(self._daily_counts.get(day_str, 0), self._target)
        self._history.add(day_str)
        return True

    def unmark_done(self, target_date: Optional[str] = None) -> bool:
        day_str = target_date or date.today().isoformat()
        self._daily_counts[day_str] = 0
        return super().unmark_done(day_str)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "countable"
        data["target"] = self._target
        data["unit"] = self.unit
        data["daily_counts"] = self._daily_counts
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountableHabit":
        habit = cls(
            name=data["name"],
            category=data.get("category", "General"),
            target=data.get("target", 1),
            unit=data.get("unit", "times"),
            created_date=data.get("created_date"),
        )
        habit._history = set(data.get("history", []))
        habit._daily_counts = data.get("daily_counts", {})
        return habit

    def __str__(self) -> str:
        today_str = date.today().isoformat()
        today_count = self.get_count(today_str)
        return (
            f"[{self.category}] {self.name} - Progress: {today_count}/{self.target} {self.unit} "
            f"(Completed {len(self._history)} days)"
        )
