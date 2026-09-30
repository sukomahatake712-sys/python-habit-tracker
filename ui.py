import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import date
from habit import HabitTracker, CountableHabit


# Color Palette (Clean Modern Dark/Teal Theme)
BG_COLOR = "#1e1e2e"
CARD_BG = "#2a2b3d"
ACCENT = "#00b4d8"
ACCENT_HOVER = "#0096c7"
SUCCESS = "#06d6a0"
SUCCESS_MUTED = "#1b4d3e"
TEXT_MAIN = "#f8f9fa"
TEXT_MUTED = "#a0aab2"
BORDER_COLOR = "#3b3d54"
HEATMAP_EMPTY = "#363852"
HEATMAP_FILLED = "#06d6a0"
CAL_BG = "#242538"
CAL_COMPLETED = "#06d6a0"
CAL_PARTIAL = "#f4a261"
CAL_NONE = "#363852"


class AddHabitDialog(tk.Toplevel):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.title("Add New Habit")
        self.geometry("420x460")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self.transient(parent)
        self.grab_set()

        self.on_submit = on_submit
        self.habit_type_var = tk.StringVar(value="boolean")

        self._build_ui()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        header = tk.Label(
            self,
            text="Create New Habit",
            font=("Segoe UI", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN,
        )
        header.pack(pady=(20, 15))

        tk.Label(self, text="Habit Name:", font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_MUTED).pack(anchor="w", padx=30)
        self.name_entry = tk.Entry(self, font=("Segoe UI", 11), bg=CARD_BG, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.name_entry.pack(fill="x", padx=30, pady=(4, 12), ipady=4)
        self.name_entry.focus()

        tk.Label(self, text="Category:", font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_MUTED).pack(anchor="w", padx=30)
        self.cat_entry = tk.Entry(self, font=("Segoe UI", 11), bg=CARD_BG, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.cat_entry.insert(0, "Health")
        self.cat_entry.pack(fill="x", padx=30, pady=(4, 12), ipady=4)

        tk.Label(self, text="Habit Type:", font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_MUTED).pack(anchor="w", padx=30)
        type_frame = tk.Frame(self, bg=BG_COLOR)
        type_frame.pack(fill="x", padx=30, pady=(4, 12))

        rb1 = tk.Radiobutton(
            type_frame,
            text="Yes/No (Boolean)",
            variable=self.habit_type_var,
            value="boolean",
            command=self._on_type_toggle,
            bg=BG_COLOR,
            fg=TEXT_MAIN,
            selectcolor=CARD_BG,
            activebackground=BG_COLOR,
            activeforeground=TEXT_MAIN,
            font=("Segoe UI", 10),
        )
        rb1.pack(side="left", padx=(0, 15))

        rb2 = tk.Radiobutton(
            type_frame,
            text="Countable Target",
            variable=self.habit_type_var,
            value="countable",
            command=self._on_type_toggle,
            bg=BG_COLOR,
            fg=TEXT_MAIN,
            selectcolor=CARD_BG,
            activebackground=BG_COLOR,
            activeforeground=TEXT_MAIN,
            font=("Segoe UI", 10),
        )
        rb2.pack(side="left")

        self.countable_frame = tk.Frame(self, bg=BG_COLOR)
        tk.Label(self.countable_frame, text="Daily Target Count:", font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_MUTED).pack(anchor="w")
        self.target_entry = tk.Entry(self.countable_frame, font=("Segoe UI", 11), bg=CARD_BG, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.target_entry.insert(0, "8")
        self.target_entry.pack(fill="x", pady=(4, 8), ipady=4)

        tk.Label(self.countable_frame, text="Unit (e.g. glasses, mins, reps):", font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_MUTED).pack(anchor="w")
        self.unit_entry = tk.Entry(self.countable_frame, font=("Segoe UI", 11), bg=CARD_BG, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.unit_entry.insert(0, "glasses")
        self.unit_entry.pack(fill="x", pady=(4, 12), ipady=4)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(fill="x", padx=30, pady=(20, 10))

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED,
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
        )
        cancel_btn.pack(side="left")

        save_btn = tk.Button(
            btn_frame,
            text="Save Habit",
            command=self._handle_save,
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT,
            fg=TEXT_MAIN,
            relief="flat",
            padx=18,
            pady=6,
            cursor="hand2",
        )
        save_btn.pack(side="right")

    def _on_type_toggle(self):
        if self.habit_type_var.get() == "countable":
            self.countable_frame.pack(fill="x", padx=30, pady=0)
        else:
            self.countable_frame.pack_forget()

    def _handle_save(self):
        name = self.name_entry.get().strip()
        cat = self.cat_entry.get().strip() or "General"
        h_type = self.habit_type_var.get()

        if not name:
            messagebox.showwarning("Validation Error", "Habit name cannot be empty.", parent=self)
            return

        target = 1
        unit = "times"
        if h_type == "countable":
            try:
                target = int(self.target_entry.get().strip())
                if target <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Validation Error", "Target must be a positive number.", parent=self)
                return
            unit = self.unit_entry.get().strip() or "times"

        if self.on_submit(name, cat, h_type, target, unit):
            self.destroy()


class HabitDetailDialog(tk.Toplevel):
    def __init__(self, parent, tracker, habit_name, on_update):
        super().__init__(parent)
        self.tracker = tracker
        self.habit_name = habit_name
        self.on_update = on_update

        self.title(f"Habit Details — {habit_name}")
        self.geometry("620x520")
        self.configure(bg=BG_COLOR)
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        stats_data = self.tracker.get_habit_stats(self.habit_name)
        if not stats_data:
            self.destroy()
            return

        header = tk.Frame(self, bg=BG_COLOR)
        header.pack(fill="x", padx=25, pady=(20, 10))

        cat_lbl = tk.Label(header, text=stats_data["category"].upper(), font=("Segoe UI", 9, "bold"), fg=ACCENT, bg=BG_COLOR)
        cat_lbl.pack(anchor="w")

        name_lbl = tk.Label(header, text=stats_data["name"], font=("Segoe UI", 18, "bold"), fg=TEXT_MAIN, bg=BG_COLOR)
        name_lbl.pack(anchor="w")

        stats_row = tk.Frame(self, bg=BG_COLOR)
        stats_row.pack(fill="x", padx=25, pady=10)

        self._create_stat_badge(stats_row, f"{stats_data['current_streak']} days", "Current Streak", side="left")
        self._create_stat_badge(stats_row, f"{stats_data['best_streak']} days", "Best Streak", side="left")
        self._create_stat_badge(stats_row, f"{stats_data['completion_rate_30d']}%", "30-Day Rate", side="left")
        self._create_stat_badge(stats_row, f"{stats_data['total_completions']}", "Total Days", side="left")

        heat_section = tk.Frame(self, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER_COLOR)
        heat_section.pack(fill="both", expand=True, padx=25, pady=15)

        heat_header = tk.Label(heat_section, text="Consistency Heatmap (Last 12 Weeks)", font=("Segoe UI", 11, "bold"), bg=CARD_BG, fg=TEXT_MAIN)
        heat_header.pack(anchor="w", padx=15, pady=(12, 6))

        canvas = tk.Canvas(heat_section, bg=CARD_BG, height=160, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self._draw_heatmap(canvas, stats_data["heatmap_matrix"])

        btn_row = tk.Frame(self, bg=BG_COLOR)
        btn_row.pack(fill="x", padx=25, pady=(0, 20))

        del_btn = tk.Button(
            btn_row,
            text="Delete Habit",
            command=self._delete_habit,
            font=("Segoe UI", 9),
            bg="#e63946",
            fg=TEXT_MAIN,
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2"
        )
        del_btn.pack(side="left")

        close_btn = tk.Button(
            btn_row,
            text="Close",
            command=self.destroy,
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg=TEXT_MAIN,
            relief="flat",
            padx=18,
            pady=5,
            cursor="hand2"
        )
        close_btn.pack(side="right")

    def _create_stat_badge(self, parent, value, label, side="left"):
        card = tk.Frame(parent, bg=CARD_BG, padx=12, pady=8, highlightthickness=1, highlightbackground=BORDER_COLOR)
        card.pack(side=side, padx=(0, 8), fill="x", expand=True)

        tk.Label(card, text=value, font=("Segoe UI", 13, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack()
        tk.Label(card, text=label, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CARD_BG).pack()

    def _draw_heatmap(self, canvas, matrix):
        cell_size = 14
        gap = 4
        start_x = 40
        start_y = 25

        day_labels = ["M", "T", "W", "T", "F", "S", "S"]
        for row, lbl in enumerate(day_labels):
            y = start_y + row * (cell_size + gap)
            canvas.create_text(start_x - 15, y + cell_size / 2, text=lbl, fill=TEXT_MUTED, font=("Segoe UI", 8))

        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                x1 = start_x + col * (cell_size + gap)
                y1 = start_y + row * (cell_size + gap)
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                is_done = matrix[row][col]
                color = HEATMAP_FILLED if is_done else HEATMAP_EMPTY
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

    def _delete_habit(self):
        if messagebox.askyesno("Confirm Delete", f"Delete '{self.habit_name}'?", parent=self):
            self.tracker.remove_habit(self.habit_name)
            self.on_update()
            self.destroy()


class CalendarView(tk.Frame):
    def __init__(self, parent, tracker, on_update):
        super().__init__(parent, bg=BG_COLOR)
        self.tracker = tracker
        self.on_update = on_update

        today = date.today()
        self.year = today.year
        self.month = today.month
        self.selected_date = today

        self._build_ui()
        self.render_month()

    def _build_ui(self):
        # Top Month Navigation Bar
        nav_bar = tk.Frame(self, bg=BG_COLOR)
        nav_bar.pack(fill="x", padx=10, pady=(10, 15))

        prev_btn = tk.Button(
            nav_bar, text="◀ Prev Month", command=self._prev_month,
            font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN, relief="flat", padx=10, pady=4, cursor="hand2"
        )
        prev_btn.pack(side="left")

        self.month_label = tk.Label(nav_bar, text="", font=("Segoe UI", 15, "bold"), fg=TEXT_MAIN, bg=BG_COLOR)
        self.month_label.pack(side="left", expand=True)

        today_btn = tk.Button(
            nav_bar, text="Today", command=self._jump_today,
            font=("Segoe UI", 9), bg=CARD_BG, fg=ACCENT, relief="flat", padx=10, pady=4, cursor="hand2"
        )
        today_btn.pack(side="right", padx=(5, 0))

        next_btn = tk.Button(
            nav_bar, text="Next Month ▶", command=self._next_month,
            font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN, relief="flat", padx=10, pady=4, cursor="hand2"
        )
        next_btn.pack(side="right")

        # Split Layout: Left is Calendar Grid, Right is Selected Day Habit Breakdown
        content_pane = tk.Frame(self, bg=BG_COLOR)
        content_pane.pack(fill="both", expand=True, padx=10, pady=0)

        # Calendar Container
        self.cal_container = tk.Frame(content_pane, bg=CAL_BG, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=12)
        self.cal_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Day Names Header
        days_header = tk.Frame(self.cal_container, bg=CAL_BG)
        days_header.pack(fill="x", pady=(0, 8))
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for d_name in day_names:
            lbl = tk.Label(days_header, text=d_name, font=("Segoe UI", 9, "bold"), fg=ACCENT, bg=CAL_BG, width=6)
            lbl.pack(side="left", expand=True, fill="x")

        # Grid of days
        self.grid_frame = tk.Frame(self.cal_container, bg=CAL_BG)
        self.grid_frame.pack(fill="both", expand=True)

        # Right Side: Day Details & Toggle Panel
        self.details_panel = tk.Frame(content_pane, bg=CARD_BG, width=240, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=15, pady=15)
        self.details_panel.pack(side="right", fill="both")
        self.details_panel.pack_propagate(False)

        self.detail_date_label = tk.Label(self.details_panel, text="", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=CARD_BG)
        self.detail_date_label.pack(anchor="w", pady=(0, 4))

        self.detail_summary_label = tk.Label(self.details_panel, text="", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG)
        self.detail_summary_label.pack(anchor="w", pady=(0, 12))

        # Habit checklist frame
        self.checklist_frame = tk.Frame(self.details_panel, bg=CARD_BG)
        self.checklist_frame.pack(fill="both", expand=True)

        # Legend at bottom of calendar
        legend_frame = tk.Frame(self.cal_container, bg=CAL_BG)
        legend_frame.pack(fill="x", pady=(10, 0))

        self._create_legend_dot(legend_frame, CAL_COMPLETED, "All Habits Done")
        self._create_legend_dot(legend_frame, CAL_PARTIAL, "Partially Done")
        self._create_legend_dot(legend_frame, CAL_NONE, "No Habits Done")

    def _create_legend_dot(self, parent, color, text):
        dot = tk.Label(parent, text="●", font=("Segoe UI", 12), fg=color, bg=CAL_BG)
        dot.pack(side="left", padx=(5, 2))
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CAL_BG)
        lbl.pack(side="left", padx=(0, 12))

    def _prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.render_month()

    def _next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.render_month()

    def _jump_today(self):
        today = date.today()
        self.year = today.year
        self.month = today.month
        self.selected_date = today
        self.render_month()

    def render_month(self):
        """Renders the calendar matrix for the current month and year."""
        month_name = calendar.month_name[self.month]
        self.month_label.config(text=f"{month_name} {self.year}")

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        cal_matrix = calendar.monthcalendar(self.year, self.month)
        habits = self.tracker.get_all_habits()
        total_habits = len(habits)

        for week_idx, week in enumerate(cal_matrix):
            week_row = tk.Frame(self.grid_frame, bg=CAL_BG)
            week_row.pack(fill="x", expand=True, pady=2)

            for day in week:
                if day == 0:
                    spacer = tk.Label(week_row, text="", bg=CAL_BG, width=6, height=2)
                    spacer.pack(side="left", expand=True, fill="both", padx=2)
                else:
                    target_date = date(self.year, self.month, day)
                    target_str = target_date.isoformat()

                    completed_count = sum(1 for h in habits if h.is_done_on(target_str))

                    if total_habits > 0 and completed_count == total_habits:
                        status_color = CAL_COMPLETED
                    elif completed_count > 0:
                        status_color = CAL_PARTIAL
                    else:
                        status_color = CAL_NONE

                    is_selected = (self.selected_date == target_date)
                    is_today = (target_date == date.today())

                    day_btn = tk.Button(
                        week_row,
                        text=f"{day}\n{'★' if is_today else '•'}",
                        font=("Segoe UI", 9, "bold" if (is_selected or is_today) else "normal"),
                        fg=TEXT_MAIN if not is_today else ACCENT,
                        bg=CARD_BG if not is_selected else "#3d4060",
                        activebackground=BORDER_COLOR,
                        activeforeground=TEXT_MAIN,
                        highlightthickness=2 if is_selected else 1,
                        highlightbackground=ACCENT if is_selected else status_color,
                        relief="flat",
                        cursor="hand2",
                        command=lambda d=target_date: self._select_date(d)
                    )
                    day_btn.pack(side="left", expand=True, fill="both", padx=2, pady=1)

        self.render_day_details()

    def _select_date(self, selected: date):
        self.selected_date = selected
        self.render_month()

    def render_day_details(self):
        """Shows detailed list of all habits on the selected date with Done / Not Done status."""
        date_str = self.selected_date.isoformat()
        formatted_date = self.selected_date.strftime("%A, %b %d, %Y")
        self.detail_date_label.config(text=formatted_date)

        for widget in self.checklist_frame.winfo_children():
            widget.destroy()

        habits = self.tracker.get_all_habits()
        if not habits:
            tk.Label(self.checklist_frame, text="No habits created yet.", fg=TEXT_MUTED, bg=CARD_BG, font=("Segoe UI", 9)).pack(pady=20)
            self.detail_summary_label.config(text="Create a habit to get started")
            return

        completed = [h for h in habits if h.is_done_on(date_str)]
        self.detail_summary_label.config(text=f"{len(completed)} of {len(habits)} habits completed")

        for habit in habits:
            is_done = habit.is_done_on(date_str)
            item_frame = tk.Frame(self.checklist_frame, bg=CARD_BG, pady=4)
            item_frame.pack(fill="x")

            status_icon = "✅" if is_done else "❌"
            tk.Label(item_frame, text=status_icon, bg=CARD_BG, font=("Segoe UI", 10)).pack(side="left", padx=(0, 5))

            name_lbl = tk.Label(
                item_frame,
                text=habit.name,
                font=("Segoe UI", 9, "bold" if is_done else "normal"),
                fg=TEXT_MAIN if is_done else TEXT_MUTED,
                bg=CARD_BG,
                anchor="w"
            )
            name_lbl.pack(side="left", fill="x", expand=True)

            toggle_btn = tk.Button(
                item_frame,
                text="Undo" if is_done else "Mark",
                font=("Segoe UI", 8),
                bg=SUCCESS_MUTED if is_done else CARD_BG,
                fg=TEXT_MAIN if is_done else ACCENT,
                relief="flat",
                highlightthickness=1,
                highlightbackground=ACCENT if not is_done else BORDER_COLOR,
                padx=6,
                pady=1,
                cursor="hand2",
                command=lambda h=habit, d=is_done: self._toggle_habit_for_date(h.name, d)
            )
            toggle_btn.pack(side="right")

    def _toggle_habit_for_date(self, habit_name: str, currently_done: bool):
        date_str = self.selected_date.isoformat()
        if currently_done:
            self.tracker.unmark_habit_done(habit_name, date_str)
        else:
            self.tracker.mark_habit_done(habit_name, date_str)

        self.on_update()
        self.render_month()

