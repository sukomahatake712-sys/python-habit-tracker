"""
stats.py - Streak & Progress Statistics Algorithms

Module Map:
- Module 3: Python Operators (arithmetic +, -, comparison ==, >=, <=, logical and, or)
- Module 5: Precedence & Associativity in Python (parenthesized expressions for date math)
- Module 8: Control Flow Statements (while, for, if-elif-else, break, continue)
- Module 9: Functions in Python (pure, testable utility functions)
- Module 11: Array data structure in Python (2D matrices, list comprehensions, slicing)
"""

from datetime import date, timedelta
from typing import Set, List, Tuple


def calculate_current_streak(history: Set[str], reference_date: date = None) -> int:
    """
    Calculates the current streak of consecutive days completed up to today (or reference_date).
    If today is completed, streak includes today.
    If today is not yet completed, but yesterday was, streak counts continuously from yesterday.
    If neither today nor yesterday was completed, streak is 0.
    """
    if not history:
        return 0

    ref = reference_date or date.today()
    today_str = ref.isoformat()
    yesterday_str = (ref - timedelta(days=1)).isoformat()

    # Determine starting anchor point
    if today_str in history:
        current_check = ref
    elif yesterday_str in history:
        current_check = ref - timedelta(days=1)
    else:
        return 0

    streak = 0
    while current_check.isoformat() in history:
        # Precedence & Associativity showcase
        streak = streak + 1
        current_check = current_check - timedelta(days=1)

    return streak


def calculate_best_streak(history: Set[str]) -> int:
    """
    Finds the longest consecutive daily streak in the history set.
    Implements consecutive sequence algorithm using sorted dates.
    """
    if not history:
        return 0

    # Type conversion: convert ISO strings to sorted date objects
    sorted_dates: List[date] = sorted([date.fromisoformat(d) for d in history])

    max_streak = 0
    current_run = 0
    prev_date = None

    for d in sorted_dates:
        if prev_date is None:
            current_run = 1
        else:
            diff_days = (d - prev_date).days
            if diff_days == 1:
                current_run = current_run + 1
            elif diff_days > 1:
                current_run = 1
            # diff_days == 0 implies duplicate day, current_run unchanged

        if current_run > max_streak:
            max_streak = current_run
        prev_date = d

    return max_streak


def calculate_completion_rate(history: Set[str], days: int = 30, reference_date: date = None) -> float:
    """
    Computes percentage of days completed within the last N days.
    Demonstrates operator math, floating point conversion, and list comprehension.
    """
    if days <= 0:
        return 0.0

    ref = reference_date or date.today()
    cutoff = ref - timedelta(days=days - 1)

    completed_in_window = sum(
        1 for d_str in history
        if date.fromisoformat(d_str) >= cutoff and date.fromisoformat(d_str) <= ref
    )

    # Precedence & Associativity in percentage formula
    rate = (completed_in_window / days) * 100.0
    return round(rate, 1)


def get_heatmap_data(history: Set[str], weeks: int = 12, end_date: date = None) -> List[List[bool]]:
    """
    Builds a 2D Array / Matrix (7 rows x N weeks) representing completion status.
    Row 0 = Monday, Row 6 = Sunday.
    Feeds visual Tkinter Canvas grid.
    """
    ref = end_date or date.today()
    # End on the most recent Sunday to make a neat grid
    days_to_sunday = (6 - ref.weekday()) % 7
    calendar_end = ref + timedelta(days=days_to_sunday)
    calendar_start = calendar_end - timedelta(weeks=weeks) + timedelta(days=1)

    # Initialize 7 x weeks 2D array (Array Data Structure module)
    matrix: List[List[bool]] = [[False for _ in range(weeks)] for _ in range(7)]

    curr = calendar_start
    col = 0
    while curr <= calendar_end and col < weeks:
        row = curr.weekday()  # 0=Monday, 6=Sunday
        if curr.isoformat() in history:
            matrix[row][col] = True

        if row == 6:  # End of week column
            col += 1
        curr += timedelta(days=1)

    return matrix
