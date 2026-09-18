# StreakKeeper — Daily Habit Streak Tracker

A desktop habit tracker built with **pure Python** demonstrating complete mastery of all foundational and intermediate Python course topics.

No HTML, CSS, JavaScript, or external third-party dependencies — built entirely with standard Python 3 and Tkinter.

---

## 📚 Module-to-Feature Map (Course Curriculum Mapping)

Every module from your Python course syllabus directly maps to practical, working features in this project:

| # | Course Module | Where it is Implemented in StreakKeeper |
|---|---|---|
| **2** | **Python Fundamentals** | Clean program structure, variables, comments, entrypoint pattern in `main.py` |
| **3** | **Python Operators** | Streak increments, arithmetic and comparison operators in `stats.py` & `tracker.py` |
| **4** | **Input and Output Operations** | JSON file read/write, safe `with open()` resource management, and `try/except` error handling in `storage.py` |
| **5** | **Precedence & Associativity** | Math calculations in streak calculations, percentage formulas, and grid coordinate mappings |
| **6** | **Type Conversion** | Converting between ISO date strings and `datetime.date`, integers, floats, and dictionaries |
| **7** | **Core Data Structures** | `dict` for indexed habit lookup, `set` for $O(1)$ completion history, `list` for ordered sequences |
| **8** | **Control Flow Statements** | Nested loops, `while` and `for` iterations, input validation, and boundary conditions |
| **9** | **Functions in Python** | Pure functions, parameter typing, callbacks, return values, and modularity in `stats.py` |
| **10** | **Modules & Packages** | Separation of concerns across `habit.py`, `storage.py`, `stats.py`, `tracker.py`, and `ui.py` |
| **11** | **Array Data Structures** | 2D matrix ($7 \times 12$) generation and nested list processing to render the visual activity heatmap |
| **12** | **Object Oriented Programming** | Base class `Habit`, subclasses `BooleanHabit` & `CountableHabit`, encapsulation (`_history`, getters/setters), polymorphism |

---

## 🗂️ Project Architecture

```
d:\Python Project\
├── main.py              # Application entry point: launches HabitTracker and Tkinter GUI
├── habit.py             # OOP Models: Habit, BooleanHabit, CountableHabit (Encapsulation, Inheritance)
├── tracker.py           # Controller: HabitTracker managing collection, auto-save, and statistics
├── storage.py           # I/O: JSON persistence and robust error handling
├── stats.py             # Algorithms: streaks, 30-day completion rates, and 2D heatmap matrix
├── ui.py                # Desktop GUI: Modern Tkinter interface, modal dialogs, and Canvas heatmap
├── test_tracker.py      # Automated unit test suite (100% passing)
├── data/
│   └── habits.json      # JSON persistence data store
└── README.md            # Comprehensive documentation and syllabus guide
```

---

## 🚀 How to Run the Project

### 1. Launch the Desktop App
Ensure you have Python 3 installed. Run:

```bash
python main.py
```

### 2. Run Automated Unit Tests
To verify all OOP models, streak calculation algorithms, and persistence:

```bash
python -m unittest test_tracker.py
```

---

## ✨ Features

- **Binary & Countable Habits**:
  - Track simple daily tasks (Meditation, Reading) or count targets (Drink 8 glasses of water).
- **Streak Calculation Engine**:
  - Automatically calculates current streak, longest best streak, and 30-day percentage completion rates.
- **Interactive Monthly Calendar View**:
  - Full interactive calendar grid color-coding days with 100% completions, partial completions, or rest days.
  - Inspect any date to view which habits were completed (✅) or missed (❌) and toggle completions on that date directly.
- **GitHub-style 12-Week Consistency Heatmap**:
  - Click any habit to inspect a 2D Canvas heatmap displaying day-by-day progress across the past 12 weeks.
- **Category Filtering**:
  - Organize and filter habits by categories (Health, Learning, Mindfulness, etc.).
- **Automatic JSON Persistence**:
  - Any habit created, marked done, or removed automatically syncs to `data/habits.json`.
