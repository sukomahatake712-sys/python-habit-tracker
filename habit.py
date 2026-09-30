import json
import os
from datetime import date, timedelta


class Habit:
    def __init__(self, name, category='General', created_date=None):
        self.name = name
        self.category = category
        self.created_date = created_date or date.today().isoformat()
        self.history = set()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Habit name cannot be empty')
        self._name = value.strip()

    def mark_done(self, target_date=None):
        day = target_date or date.today().isoformat()
        self.history.add(day)
        return True

    def unmark_done(self, target_date=None):
        day = target_date or date.today().isoformat()
        if day in self.history:
            self.history.remove(day)
            return True
        return False

    def is_done_today(self):
        return date.today().isoformat() in self.history

    def is_done_on(self, day_str):
        return day_str in self.history

    def to_dict(self):
        return {
            'type': 'boolean',
            'name': self._name,
            'category': self.category,
            'created_date': self.created_date,
            'history': sorted(list(self.history))
        }

    @classmethod
    def from_dict(cls, data):
        if data.get('type') == 'countable':
            return CountableHabit.from_dict(data)
        return BooleanHabit.from_dict(data)


class BooleanHabit(Habit):
    @classmethod
    def from_dict(cls, data):
        habit = cls(data['name'], data.get('category', 'General'), data.get('created_date'))
        habit.history = set(data.get('history', []))
        return habit


class CountableHabit(Habit):
    def __init__(self, name, category='General', target=1, unit='times', created_date=None):
        super().__init__(name, category, created_date)
        self.target = target
        self.unit = unit
        self.daily_counts = {}

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, val):
        if not isinstance(val, int) or val <= 0:
            raise ValueError('Target must be a positive number')
        self._target = val

    def get_count(self, target_date=None):
        day = target_date or date.today().isoformat()
        return self.daily_counts.get(day, 0)

    def record_progress(self, amount=1, target_date=None):
        day = target_date or date.today().isoformat()
        total = self.daily_counts.get(day, 0) + amount
        self.daily_counts[day] = total
        if total >= self.target:
            self.history.add(day)
            return True
        return False

    def mark_done(self, target_date=None):
        day = target_date or date.today().isoformat()
        self.daily_counts[day] = max(self.daily_counts.get(day, 0), self.target)
        self.history.add(day)
        return True

    def unmark_done(self, target_date=None):
        day = target_date or date.today().isoformat()
        self.daily_counts[day] = 0
        return super().unmark_done(day)

    def to_dict(self):
        data = super().to_dict()
        data['type'] = 'countable'
        data['target'] = self.target
        data['unit'] = self.unit
        data['daily_counts'] = self.daily_counts
        return data

    @classmethod
    def from_dict(cls, data):
        habit = cls(
            data['name'],
            data.get('category', 'General'),
            data.get('target', 1),
            data.get('unit', 'times'),
            data.get('created_date')
        )
        habit.history = set(data.get('history', []))
        habit.daily_counts = data.get('daily_counts', {})
        return habit


def calculate_current_streak(history, reference_date=None):
    if not history:
        return 0
    ref = reference_date or date.today()
    today_str = ref.isoformat()
    yesterday_str = (ref - timedelta(days=1)).isoformat()

    if today_str in history:
        curr = ref
    elif yesterday_str in history:
        curr = ref - timedelta(days=1)
    else:
        return 0

    streak = 0
    while curr.isoformat() in history:
        streak += 1
        curr -= timedelta(days=1)
    return streak


def calculate_best_streak(history):
    if not history:
        return 0
    sorted_days = sorted([date.fromisoformat(d) for d in history])
    best = 0
    current = 0
    prev = None

    for d in sorted_days:
        if prev is None:
            current = 1
        else:
            diff = (d - prev).days
            if diff == 1:
                current += 1
            elif diff > 1:
                current = 1
        if current > best:
            best = current
        prev = d
    return best


def calculate_completion_rate(history, days=30, reference_date=None):
    if days <= 0:
        return 0.0
    ref = reference_date or date.today()
    cutoff = ref - timedelta(days=days - 1)
    completed = sum(1 for d in history if cutoff <= date.fromisoformat(d) <= ref)
    return round((completed / days) * 100, 1)


def get_heatmap_data(history, weeks=12, end_date=None):
    ref = end_date or date.today()
    days_to_sunday = (6 - ref.weekday()) % 7
    cal_end = ref + timedelta(days=days_to_sunday)
    cal_start = cal_end - timedelta(weeks=weeks) + timedelta(days=1)

    grid = [[False for _ in range(weeks)] for _ in range(7)]
    curr = cal_start
    col = 0
    while curr <= cal_end and col < weeks:
        row = curr.weekday()
        if curr.isoformat() in history:
            grid[row][col] = True
        if row == 6:
            col += 1
        curr += timedelta(days=1)
    return grid


class HabitTracker:
    def __init__(self, filepath='data/habits.json'):
        self.filepath = filepath
        self.habits = self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {k: Habit.from_dict(v) for k, v in data.items()}
        except Exception:
            return {}

    def save(self):
        os.makedirs(os.path.dirname(self.filepath) or '.', exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump({k: v.to_dict() for k, v in self.habits.items()}, f, indent=2)

    def add_boolean_habit(self, name, category='General'):
        if name in self.habits:
            raise ValueError(f'Habit {name} already exists')
        habit = BooleanHabit(name, category)
        self.habits[name] = habit
        self.save()
        return habit

    def add_countable_habit(self, name, target, unit='times', category='General'):
        if name in self.habits:
            raise ValueError(f'Habit {name} already exists')
        habit = CountableHabit(name, category, target, unit)
        self.habits[name] = habit
        self.save()
        return habit

    def remove_habit(self, name):
        if name in self.habits:
            del self.habits[name]
            self.save()
            return True
        return False

    def get_habit(self, name):
        return self.habits.get(name)

    def get_all_habits(self):
        return sorted(self.habits.values(), key=lambda h: (h.category, h.name))

    def get_habits_by_category(self, category):
        return [h for h in self.habits.values() if h.category.lower() == category.lower()]

    def get_categories(self):
        cats = {h.category for h in self.habits.values()}
        return sorted(list(cats)) if cats else ['General']

    def mark_habit_done(self, name, date_str=None):
        habit = self.get_habit(name)
        if habit:
            res = habit.mark_done(date_str)
            self.save()
            return res
        return False

    def unmark_habit_done(self, name, date_str=None):
        habit = self.get_habit(name)
        if habit:
            res = habit.unmark_done(date_str)
            self.save()
            return res
        return False

    def record_habit_progress(self, name, amount=1, date_str=None):
        habit = self.get_habit(name)
        if not habit:
            return False
        if isinstance(habit, CountableHabit):
            res = habit.record_progress(amount, date_str)
        else:
            res = habit.mark_done(date_str)
        self.save()
        return res

    def get_habit_stats(self, name):
        habit = self.get_habit(name)
        if not habit:
            return {}
        h = habit.history
        return {
            'name': habit.name,
            'category': habit.category,
            'is_done_today': habit.is_done_today(),
            'total_completions': len(h),
            'current_streak': calculate_current_streak(h),
            'best_streak': calculate_best_streak(h),
            'completion_rate_30d': calculate_completion_rate(h, 30),
            'completion_rate_7d': calculate_completion_rate(h, 7),
            'heatmap_matrix': get_heatmap_data(h, 12),
        }
