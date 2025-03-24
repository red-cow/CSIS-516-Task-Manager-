import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime
import sqlite3


class TaskCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar")

        # Database Connection
        self.conn = sqlite3.connect("TaskManager.db")
        self.cursor = self.conn.cursor()

        # Calendar Frame
        self.frames = {"calendar": tk.Frame(root)}
        self.frames["calendar"].pack(pady=20)

        # Calendar Label
        lbl_calendar = tk.Label(self.frames["calendar"], text="📅 Calendar View", font=("Arial", 14, "bold"))
        lbl_calendar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        # Calendar Widget
        self.cal = Calendar(self.frames["calendar"], selectmode="day", date_pattern="yyyy-MM-dd")
        self.cal.grid(row=1, column=0, columnspan=2, pady=10)

        # Highlight Task Dates
        self.highlight_task_dates()

        # Buttons
        btn_show_tasks = tk.Button(self.frames["calendar"], text="📜 Show Tasks", command=self.show_tasks)
        btn_show_tasks.grid(row=2, column=0, pady=10)

        btn_add_task = tk.Button(self.frames["calendar"], text="➕ Add Task", command=self.add_task)
        btn_add_task.grid(row=2, column=1, pady=10)

        # Task Display Label
        self.task_label = tk.Label(self.frames["calendar"], text="Tasks for Selected Date:\n", justify="left",
                                   font=("Arial", 12))
        self.task_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Back Button
        btn_back = tk.Button(self.frames["calendar"], text="🔙 Back", command=self.go_back)
        btn_back.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

    def highlight_task_dates(self):
        """Highlight due dates with priority colors in the calendar."""
        try:
            self.cursor.execute("SELECT DISTINCT due_date, Priority FROM Task WHERE due_date IS NOT NULL")
            task_dates = self.cursor.fetchall()

            # Define priority colors
            priority_colors = {"High": "red", "Medium": "orange", "Low": "blue"}

            # Configure tags for each priority level (avoid redundant calls in loop)
            for priority, color in priority_colors.items():
                if not self.cal.tag_has(f"task_{priority}"):
                    self.cal.tag_config(f"task_{priority}", background=color, foreground="white")

            # Iterate through tasks and add events
            for date, priority in task_dates:
                try:
                    parsed_date = datetime.strptime(date, "%Y-%m-%d")
                    self.cal.calevent_create(parsed_date, "Task Due", f"task_{priority}")
                except ValueError:
                    print(f"Skipping invalid date format: {date}")

        except Exception as e:
            print(f"Error highlighting task dates: {e}")

    def show_tasks(self):
        """Fetch and display tasks for the selected date."""
        selected_date = self.cal.get_date()
        self.cursor.execute("SELECT ID, Title, Description, Priority FROM Task WHERE DueDate = ?", (selected_date,))
        tasks = self.cursor.fetchall()

        if tasks:
            task_text = f"🗓 Tasks for {selected_date}:\n" + "\n".join(
                [f"📌 {title} ({priority})\n  - {desc} [📝 Edit / ❌ Delete]" for _, title, desc, priority in tasks]
            )
        else:
            task_text = f"No tasks found for {selected_date}."

        self.task_label.config(text=task_text)

        # Add edit/delete functionality
        for task_id, title, desc, priority in tasks:
            btn_edit = tk.Button(self.frames["calendar"], text="📝", command=lambda t=task_id: self.edit_task(t))
            btn_edit.grid()
            btn_delete = tk.Button(self.frames["calendar"], text="❌", command=lambda t=task_id: self.delete_task(t))
            btn_delete.grid()

    def add_task(self):
        """Add a new task."""
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if not title:
            return

        description = simpledialog.askstring("Add Task", "Enter task description:")
        priority = simpledialog.askstring("Add Task", "Enter priority (High, Medium, Low):", initialvalue="Medium")
        if priority not in ("High", "Medium", "Low"):
            messagebox.showerror("Error", "Priority must be High, Medium, or Low.")
            return

        due_date = self.cal.get_date()
        self.cursor.execute("INSERT INTO Task (Title, Description, DueDate, Priority) VALUES (?, ?, ?, ?)",
                            (title, description, due_date, priority))
        self.conn.commit()
        self.highlight_task_dates()
        self.show_tasks()
        messagebox.showinfo("Success", "Task added successfully!")

    def edit_task(self, task_id):
        """Edit an existing task."""
        new_title = simpledialog.askstring("Edit Task", "Enter new task title:")
        if not new_title:
            return

        new_description = simpledialog.askstring("Edit Task", "Enter new task description:")
        new_priority = simpledialog.askstring("Edit Task", "Enter priority (High, Medium, Low):", initialvalue="Medium")
        if new_priority not in ("High", "Medium", "Low"):
            messagebox.showerror("Error", "Priority must be High, Medium, or Low.")
            return

        self.cursor.execute("UPDATE Task SET Title = ?, Description = ?, Priority = ? WHERE ID = ?",
                            (new_title, new_description, new_priority, task_id))
        self.conn.commit()
        self.highlight_task_dates()
        self.show_tasks()
        messagebox.showinfo("Success", "Task updated successfully!")

    def delete_task(self, task_id):
        """Delete a task."""
        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            self.cursor.execute("DELETE FROM Task WHERE ID = ?", (task_id,))
            self.conn.commit()
            self.highlight_task_dates()
            self.show_tasks()
            messagebox.showinfo("Success", "Task deleted successfully!")

    def go_back(self):
        print("Closing application...")
        self.master.destroy()

# Run the Application
root = tk.Tk()
app = TaskCalendarApp(root)
root.mainloop()
