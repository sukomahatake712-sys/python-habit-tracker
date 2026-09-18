"""
main.py - StreakKeeper Application Entry Point

Module Map:
- Module 2: Python Fundamentals (startup execution, standard entrypoint pattern)
- Module 10: Modules & Packages (integrating ui, tracker into single execution)
"""

import tkinter as tk
import os
from tracker import HabitTracker
from ui import StreakKeeperApp


def main():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Initialize backend tracker
    tracker = HabitTracker(filepath="data/habits.json")

    # Launch Tkinter GUI
    root = tk.Tk()
    app = StreakKeeperApp(root, tracker)
    root.mainloop()


if __name__ == "__main__":
    main()
