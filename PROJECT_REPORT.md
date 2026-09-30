# Project Report: StreakKeeper Habit Tracker

**Author**: Sukoma Hatake  
**Project**: StreakKeeper — Desktop Habit & Streak Tracker  
**Language**: Python 3 (Tkinter GUI, JSON Storage)  
**Date**: September 2026  

---

## 1. Executive Summary

StreakKeeper is a standalone desktop habit tracking application written entirely in pure Python. The goal of the project was to develop a functional personal productivity tool applying core computer science and software development principles learned across the curriculum—including Object-Oriented Programming (OOP), file I/O, algorithm design, collection data structures, and graphical user interface (GUI) development.

The application allows users to define custom habits, track daily completion, monitor consecutive-day streaks, inspect habit completion through an interactive calendar, and view consistency over a 12-week GitHub-style heatmap.

---

## 2. Key Objectives & Learning Outcomes

The project directly reinforces the foundational modules of computer programming in Python:

1. **Object-Oriented Programming**:
   - Base `Habit` class encapsulates state (`_name`, `history`, `created_date`) with input validation via getters and setters.
   - Subclasses `BooleanHabit` and `CountableHabit` implement inheritance and polymorphism, overriding `to_dict()`, `from_dict()`, and `mark_done()` behaviors.
2. **Data Structures**:
   - Sets (`set`) enable $O(1)$ daily completion lookups and duplicate-free history tracking.
   - Dictionaries (`dict`) provide $O(1)$ habit retrieval and structured JSON serialization.
   - Two-dimensional lists (`list[list[bool]]`) represent matrices for calendar and heatmap views.
3. **Algorithms & Logic**:
   - Backward date walk with `datetime.timedelta` to determine active consecutive daily streaks.
   - Longest consecutive sequence detection to compute best all-time streaks.
   - Windowed percentage aggregation for 7-day and 30-day completion rates.
4. **File I/O & Persistence**:
   - Clean, safe reads and writes with Python's built-in `json` module, ensuring graceful error recovery on corrupted or missing storage files.
5. **Desktop GUI Engineering**:
   - Event-driven interface using Tkinter with view-switching (Habit Cards view vs. Interactive Monthly Calendar view) and custom `Canvas` drawing for data visualisations.

---

## 3. System Architecture

The project follows a streamlined, maintainable architecture:

```
StreakKeeper/
├── main.py            # Entry point initializing the application controller & GUI
├── habit.py           # Domain models, streak algorithms, and JSON storage logic
├── ui.py              # Tkinter desktop frontend (Cards, Calendar, Modals, Canvas)
├── test_tracker.py    # Automated test suite verifying business logic
└── data/
    └── habits.json    # Persistent JSON storage file
```

### 3.1 Domain Logic (`habit.py`)
- **`Habit`**: Defines habit attributes, validation, completion toggling, and serialization.
- **`BooleanHabit`**: Represents binary done/not-done tasks (e.g., Reading, Meditation).
- **`CountableHabit`**: Tracks numerical progress increments toward daily goals (e.g., 8 glasses of water).
- **Streak Calculation**: Pure functions (`calculate_current_streak`, `calculate_best_streak`, `calculate_completion_rate`, `get_heatmap_data`) operating on date sets without side effects.
- **`HabitTracker`**: Manages habit collections and persists state changes to `data/habits.json`.

### 3.2 User Interface (`ui.py`)
- **`StreakKeeperApp`**: Main root window with navigation controls and category filters.
- **`CalendarView`**: Interactive monthly grid showing daily completion badges with a date detail inspector panel.
- **`AddHabitDialog`**: Modal dialog for creating Boolean or Countable habits with input validation.
- **`HabitDetailDialog`**: Detail popup featuring statistics cards and an activity heatmap rendered via Tkinter `Canvas`.

---

## 4. Verification and Testing

Automated test cases in `test_tracker.py` validate all business rules:
- **Validation**: Rejection of empty habit names.
- **Polymorphism**: Progression and completion verification for both boolean and countable habit instances.
- **Streak Edge Cases**: Testing streaks with missing days, broken runs, today-uncompleted sequences, and best-streak determination.
- **Roundtrip Persistence**: Saving to a temporary file and reloading to confirm zero data loss.

**Test Run Output**:
```
Ran 8 tests in 0.010s
OK
```

---

## 5. Conclusion

StreakKeeper successfully fulfills the objectives of the course by synthesizing language fundamentals, data structures, algorithms, and OOP into an intuitive, dependency-free application. The clean modular structure and automated tests ensure the project is easy to maintain and expand with future enhancements (such as notifications or data export).
