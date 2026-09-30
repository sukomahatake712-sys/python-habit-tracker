import os
import tkinter as tk
from habit import HabitTracker
from ui import StreakKeeperApp


def main():
    os.makedirs("data", exist_ok=True)
    tracker = HabitTracker("data/habits.json")
    root = tk.Tk()
    app = StreakKeeperApp(root, tracker)
    root.mainloop()


if __name__ == "__main__":
    main()
