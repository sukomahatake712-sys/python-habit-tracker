"""
storage.py - File I/O & Persistence Layer

Module Map:
- Module 4: Input and Output operations in Python (open, read, write JSON files, exceptions)
- Module 6: Type Conversion (parsing ISO dates, type casting, dict serializations)
- Module 7: Core Data Structures (dict, list, set manipulation)
"""

import json
import os
from typing import Dict, Any
from habit import Habit


def load_habits(filepath: str = "data/habits.json") -> Dict[str, Habit]:
    """
    Loads habits from the JSON storage file.
    Demonstrates file I/O, error handling, and conversion back to domain objects.
    """
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        habits = {}
        for name, h_data in raw_data.items():
            habits[name] = Habit.from_dict(h_data)
        return habits
    except (json.JSONDecodeError, OSError) as e:
        print(f"[Warning] Could not parse habit storage file '{filepath}': {e}. Returning empty tracker.")
        return {}


def save_habits(filepath: str, habits: Dict[str, Habit]) -> bool:
    """
    Saves habits dictionary to a JSON file.
    Creates parent directories if they do not exist.
    """
    try:
        dirname = os.path.dirname(filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        serializable_data = {name: h.to_dict() for name, h in habits.items()}

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        return True
    except OSError as e:
        print(f"[Error] Failed to save habits to '{filepath}': {e}")
        return False
