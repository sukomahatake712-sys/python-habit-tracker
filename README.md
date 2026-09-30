# StreakKeeper - Python Habit & Streak Tracker

StreakKeeper is a lightweight desktop habit tracker built with Python and Tkinter. It helps you build consistent daily habits through streak tracking, interactive monthly calendars, and 12-week activity heatmaps without requiring external dependencies or web servers.

---

## Features

- **Habit Types**:
  - **Yes/No Habits**: Simple completion toggle for tasks like reading or meditation.
  - **Countable Habits**: Step-by-step progress tracking toward daily targets (e.g. 8 glasses of water).
- **Streak & Statistics Engine**:
  - Real-time calculation of current streak and all-time best streak.
  - 7-day and 30-day completion percentage rates.
- **Interactive Monthly Calendar**:
  - Visual color badges showing daily completion status (all completed, partial, or none).
  - Inspect any date to view which habits were completed or missed, with direct mark/undo toggles.
- **12-Week Consistency Heatmap**:
  - GitHub-style activity grid visualising consistency across the last 12 weeks.
- **Local Persistence**:
  - Automatic JSON persistence to `data/habits.json` on every change.

---

## Project Structure

```
├── main.py            # App launcher & Tkinter setup
├── habit.py           # Core logic: Habit classes, streak algorithms & JSON storage
├── ui.py              # Tkinter GUI: cards view, detail popup, monthly calendar
├── test_tracker.py    # Unit tests for models and streak calculation
├── data/
│   └── habits.json    # Local habit database
└── README.md
```

---

## Getting Started

### Requirements
- Python 3.8+ (Tkinter is included with standard Python installations on Windows/macOS)

### Running the Application
```bash
python main.py
```

### Running Unit Tests
```bash
python -m unittest test_tracker.py
```
