import tkinter as tk
from tkinter import Toplevel
from tkcalendar import Calendar
from datetime import datetime
from src.Style import UIStyle
class PickDate:
    def open_date_picker(self):
        date_window = Toplevel(self.root)
        date_window.title("Select a Date")
        date_window.grab_set()  # Make this window modal (blocks interaction with the main window)
        date_window.focus_force()  # Force focus on this window
        date_window.config(bg=UIStyle.COLORS["bg"])

        # Calendar widget
        cal = Calendar(date_window, selectmode="day", date_pattern="yyyy-mm-dd", mindate=datetime.today().date())
        UIStyle.apply_calendar_style(cal)
        cal.pack(pady=20)

        # Confirm Button
        def set_date():
            selected_date = cal.get_date()
            UIStyle.apply_label_style(self.date_label_task_created, text=f"Selected Date: {selected_date}", font="body")
            date_window.destroy()

        btn_close = tk.Button(date_window)
        btn_close.pack(pady=10)
        UIStyle.apply_button_style(btn_close, text="Confirm Date", command=set_date)