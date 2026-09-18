"""
test_tracker.py - Automated Unit Test Suite for StreakKeeper

Validates:
- Habit OOP model, encapsulation, inheritance, countable targets
- Streak calculations (consecutive, gaps, best streak)
- Heatmap 2D matrix structure
- File persistence & recovery
"""

import unittest
import os
import tempfile
from datetime import date, timedelta
from habit import Habit, BooleanHabit, CountableHabit
import stats
import storage
from tracker import HabitTracker


class TestHabitModels(unittest.TestCase):
    def test_habit_validation(self):
        with self.assertRaises(ValueError):
            Habit("")
        with self.assertRaises(ValueError):
            Habit("   ")

    def test_boolean_habit(self):
        h = BooleanHabit(name="Reading", category="Learning")
        self.assertEqual(h.name, "Reading")
        self.assertEqual(h.category, "Learning")
        self.assertFalse(h.is_done_today())

        h.mark_done()
        self.assertTrue(h.is_done_today())
        self.assertEqual(len(h.history), 1)

        h.unmark_done()
        self.assertFalse(h.is_done_today())

    def test_countable_habit(self):
        ch = CountableHabit(name="Drink Water", target=4, unit="glasses")
        today = date.today().isoformat()
        
        # 1 glass - not done yet
        is_done = ch.record_progress(1)
        self.assertFalse(is_done)
        self.assertEqual(ch.get_count(), 1)
        self.assertFalse(ch.is_done_today())

        # reach target
        is_done = ch.record_progress(3)
        self.assertTrue(is_done)
        self.assertEqual(ch.get_count(), 4)
        self.assertTrue(ch.is_done_today())


class TestStreakAlgorithms(unittest.TestCase):
    def test_current_streak(self):
        ref = date(2026, 9, 18)
        # Completed today, yesterday, 2 days ago = 3 day streak
        history = {
            "2026-09-18",
            "2026-09-17",
            "2026-09-16",
        }
        self.assertEqual(stats.calculate_current_streak(history, reference_date=ref), 3)

        # Gap on 2026-09-15, completed 2026-09-14 -> still 3
        history.add("2026-09-14")
        self.assertEqual(stats.calculate_current_streak(history, reference_date=ref), 3)

        # Today not completed, yesterday completed -> streak intact
        history_no_today = {"2026-09-17", "2026-09-16"}
        self.assertEqual(stats.calculate_current_streak(history_no_today, reference_date=ref), 2)

        # Broken streak (neither today nor yesterday)
        history_broken = {"2026-09-15"}
        self.assertEqual(stats.calculate_current_streak(history_broken, reference_date=ref), 0)

    def test_best_streak(self):
        history = {
            "2026-09-01", "2026-09-02", "2026-09-03", # 3 days
            "2026-09-10", "2026-09-11", "2026-09-12", "2026-09-13", "2026-09-14", # 5 days
            "2026-09-20" # 1 day
        }
        self.assertEqual(stats.calculate_best_streak(history), 5)

    def test_completion_rate(self):
        ref = date(2026, 9, 18)
        # 3 completions in 10 days = 30.0%
        history = {"2026-09-18", "2026-09-17", "2026-09-16"}
        rate = stats.calculate_completion_rate(history, days=10, reference_date=ref)
        self.assertEqual(rate, 30.0)

    def test_heatmap_matrix(self):
        matrix = stats.get_heatmap_data(set(), weeks=12)
        # 7 rows (M-Sun) x 12 cols
        self.assertEqual(len(matrix), 7)
        for row in matrix:
            self.assertEqual(len(row), 12)


class TestPersistence(unittest.TestCase):
    def test_save_and_load_roundtrip(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            tracker = HabitTracker(filepath=temp_path)
            tracker.add_boolean_habit("Meditation", "Wellness")
            tracker.add_countable_habit("Pushups", target=50, unit="reps", category="Fitness")

            tracker.mark_habit_done("Meditation")
            tracker.record_habit_progress("Pushups", 50)

            # Re-read in fresh tracker
            tracker2 = HabitTracker(filepath=temp_path)
            self.assertIn("Meditation", tracker2._habits)
            self.assertIn("Pushups", tracker2._habits)
            self.assertTrue(tracker2.get_habit("Meditation").is_done_today())
            self.assertTrue(tracker2.get_habit("Pushups").is_done_today())
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
