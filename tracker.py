"""
tracker.py - Tracker Manager (Application Controller)

Module Map:
- Module 9: Functions in Python (cleanly partitioned operational methods)
- Module 10: Modules & Packages in Python (importing across storage, stats, habit)
- Module 12: OOP in Python (encapsulation of domain state)
"""

from typing import Dict, List, Optional
from habit import Habit, BooleanHabit, CountableHabit
import storage
import stats


class HabitTracker:
    """
    Coordinates habit lifecycle, statistics calculation, and automated persistence.
    """

    def __init__(self, filepath: str = "data/habits.json"):
        self.filepath = filepath
        self._habits: Dict[str, Habit] = storage.load_habits(self.filepath)

    def save(self) -> bool:
        """Persists current tracker state to disk."""
        return storage.save_habits(self.filepath, self._habits)

    def add_boolean_habit(self, name: str, category: str = "General") -> BooleanHabit:
        """Creates and persists a new BooleanHabit."""
        if name in self._habits:
            raise ValueError(f"Habit '{name}' already exists.")
        habit = BooleanHabit(name=name, category=category)
        self._habits[name] = habit
        self.save()
        return habit

    def add_countable_habit(self, name: str, target: int, unit: str = "reps", category: str = "General") -> CountableHabit:
        """Creates and persists a new CountableHabit."""
        if name in self._habits:
            raise ValueError(f"Habit '{name}' already exists.")
        habit = CountableHabit(name=name, category=category, target=target, unit=unit)
        self._habits[name] = habit
        self.save()
        return habit

    def remove_habit(self, name: str) -> bool:
        """Deletes a habit and saves."""
        if name in self._habits:
            del self._habits[name]
            self.save()
            return True
        return False

    def get_habit(self, name: str) -> Optional[Habit]:
        """Retrieves a single habit by name."""
        return self._habits.get(name)

    def get_all_habits(self) -> List[Habit]:
        """Returns all habits sorted by category and name."""
        return sorted(self._habits.values(), key=lambda h: (h.category, h.name))

    def get_habits_by_category(self, category: str) -> List[Habit]:
        """Filters habits by category."""
        return [h for h in self._habits.values() if h.category.lower() == category.lower()]

    def get_categories(self) -> List[str]:
        """Returns a sorted list of unique categories."""
        cats = {h.category for h in self._habits.values()}
        return sorted(list(cats)) if cats else ["General"]

    def mark_habit_done(self, name: str, date_str: Optional[str] = None) -> bool:
        """Marks habit as done and saves."""
        habit = self.get_habit(name)
        if not habit:
            return False
        result = habit.mark_done(date_str)
        self.save()
        return result

    def unmark_habit_done(self, name: str, date_str: Optional[str] = None) -> bool:
        """Unmarks habit done for the date and saves."""
        habit = self.get_habit(name)
        if not habit:
            return False
        result = habit.unmark_done(date_str)
        self.save()
        return result

    def record_habit_progress(self, name: str, amount: int = 1, date_str: Optional[str] = None) -> bool:
        """Records progress on a CountableHabit and saves."""
        habit = self.get_habit(name)
        if not habit:
            return False
        if isinstance(habit, CountableHabit):
            result = habit.record_progress(amount, date_str)
            self.save()
            return result
        else:
            return self.mark_habit_done(name, date_str)

    def get_habit_stats(self, name: str) -> Dict[str, any]:
        """Returns computed statistical metrics for a habit."""
        habit = self.get_habit(name)
        if not habit:
            return {}

        history = habit.history
        current_streak = stats.calculate_current_streak(history)
        best_streak = stats.calculate_best_streak(history)
        completion_30d = stats.calculate_completion_rate(history, days=30)
        completion_7d = stats.calculate_completion_rate(history, days=7)
        heatmap_matrix = stats.get_heatmap_data(history, weeks=12)

        return {
            "name": habit.name,
            "category": habit.category,
            "is_done_today": habit.is_done_today(),
            "total_completions": len(history),
            "current_streak": current_streak,
            "best_streak": best_streak,
            "completion_rate_30d": completion_30d,
            "completion_rate_7d": completion_7d,
            "heatmap_matrix": heatmap_matrix,
        }
