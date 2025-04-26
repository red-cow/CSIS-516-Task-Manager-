import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from src.CalendarPicker import PickDate
from tkcalendar import Calendar
from datetime import datetime
from src.Style import UIStyle


class TaskCalendarApp:

    def main(self, parentFrame, parentObject):
        self.root = parentObject.root
        self.object = parentObject
        self.frame = parentFrame
        self.pointer = 0

        parentFrame.grid_columnconfigure(0, weight=1)
        parentFrame.grid_columnconfigure(6, weight=1)

        # Calendar Label
        lbl_calendar = tk.Label(parentFrame)  #, text="📅 Calendar View", font=("Arial", 14, "bold"))
        lbl_calendar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        UIStyle.apply_label_style(lbl_calendar, text="📅 Calendar View", font="heading")

        lbl_selected = tk.Label(parentFrame)  #, text="📅 Calendar View", font=("Arial", 14, "bold"))
        lbl_selected.grid(row=0, column=2, columnspan=2, sticky="ew", pady=10)
        UIStyle.apply_label_style(lbl_selected, text="Selected Task", font="heading")

        # Calendar Widget
        self.cal = Calendar(parentFrame, selectmode="day", date_pattern="M/D/YY")
        self.cal.grid(row=1, column=0, columnspan=2, pady=10)
        self.cal.bind("<<CalendarSelected>>", lambda event: self.show_tasks(parentObject, parentFrame))

        # Highlight Task Dates
        self.highlight_task_dates(parentObject)

        # Buttons
        btn_show_tasks = tk.Button(parentFrame)  #, command=self.show_tasks)
        btn_show_tasks.grid(row=5, column=0, pady=10)
        UIStyle.apply_button_style(btn_show_tasks, text="📜 Show Tasks",
                                   command=lambda: parentObject.show_frame("list_view"))

        btn_add_task = tk.Button(parentFrame)  #, command=self.add_task)
        btn_add_task.grid(row=5, column=1, pady=10)
        UIStyle.apply_button_style(btn_add_task, text="➕ Add Task",
                                   command=lambda: parentObject.show_frame("create_task"))

        # Scrollable Canvas for Task Display
        self.task_canvas = tk.Canvas(parentFrame, width=400, bg=UIStyle.COLORS["bg"], highlightthickness=0)
        self.task_canvas.grid(row=1, column=2, columnspan=2, rowspan=4, sticky="nsew", pady=10)

        scrollbar = tk.Scrollbar(parentFrame, orient="vertical", command=self.task_canvas.yview)
        scrollbar.grid(row=1, column=4, rowspan=4, sticky="ns", pady=10)

        self.task_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside the canvas
        self.task_inner_frame = tk.Frame(self.task_canvas, bg=UIStyle.COLORS["bg"])
        self.task_window = self.task_canvas.create_window((0, 0), window=self.task_inner_frame, anchor="nw")

        # Configure scrolling
        def on_frame_configure(event):
            self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all"))

        self.task_inner_frame.bind("<Configure>", on_frame_configure)
        self.task_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Back Button
        btn_back = tk.Button(parentFrame)  #, command=self.go_back)
        btn_back.grid(row=5, column=3, columnspan=2, sticky="ew", pady=50)
        UIStyle.apply_button_style(btn_back, text="🔙 Back", command=lambda: parentObject.show_frame("home"),
                                   bg="danger")
    def __init__(self, parentFrame, parentObject):
        self.main(parentFrame, parentObject)

    def highlight_task_dates(self, parentObject):
        try:
            task_dates = parentObject.db.HighlightTaskDate(email=parentObject.user[0])
            print(task_dates)

            # Define priority colors
            priority_colors = {
                "Critical": "red",  # Bright Red
                "High": "orange",  # Vivid Orange
                "Medium": "#FFD700",  # Strong Yellow (Gold)
                "Low": "#ADD8E6"  # Light Blue (classic)
            }

            for event_id in self.cal.get_calevents():
                self.cal.calevent_remove(event_id)

            # Configure events based on priority
            for date, priority in task_dates:
                try:
                    # Parse using strptime
                    parsed_date = datetime.strptime(date, "%m/%d/%y").date()

                    # Create event using 'tags' argument
                    self.cal.calevent_create(
                        parsed_date,  # Already a date instance
                        "Task Due",
                        tags=[f"task_{priority}"]
                    )

                    # Configure color for the priority
                    self.cal.tag_config(f"task_{priority}", background=priority_colors.get(priority, "gray"))

                except ValueError:
                    print(f"Skipping invalid date format: {date}")

        except Exception as e:
            print(f"Error highlighting task dates: {e}")

    def show_tasks(self, parentObject, parentFrame):
        selected_date = self.cal.get_date()
        print(parentObject.user[0])
        tasks = parentObject.db.GetTaskByDate(selected_date, parentObject.user[0])

        for widget in self.task_inner_frame.winfo_children():
            widget.destroy()

        print(tasks)
        if not tasks:
            temp_label = tk.Label(self.task_inner_frame)
            temp_label.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
            UIStyle.apply_label_style(
                temp_label,
                text=f"Nothing found for {selected_date}",
                font="body",
                max_width=380
            )

        for i, task in enumerate(tasks):
            task_id = task[1]
            print(task_id)

            # Task Label
            task_label = tk.Label(self.task_inner_frame)
            task_label.grid(row=i * 4, column=0, columnspan=2, pady=5)
            UIStyle.apply_label_style(
                task_label,
                text=f"📌 Title: {task[3]}\n Priority: {task[0]}\n  Description: {task[2]}",
                font="body",
                max_width=380
            )

            # Edit Button
            btn_edit = tk.Button(self.task_inner_frame)
            btn_edit.grid(row=i * 4 + 1, column=0, padx=5)
            UIStyle.apply_button_style(
                btn_edit,
                text="📝 Edit Task",
                command=lambda t=task: self.edit_task2((t)),
                bg="primary"
            )

            # Delete Button
            btn_delete = tk.Button(self.task_inner_frame)
            btn_delete.grid(row=i * 4 + 1, column=1, padx=5)
            UIStyle.apply_button_style(
                btn_delete,
                text="❌ Delete Task",
                command=lambda t=task: self.delete_task(t),
                bg="danger"
            )

            # 🔹 Breaker line
            separator = ttk.Separator(self.task_inner_frame, orient="horizontal")
            separator.grid(row=i * 4 + 2, column=0, columnspan=2, sticky="ew", pady=10)

    def edit_task2(self, task):
        priority = task[0]
        task_id = task[1]
        description = task[2]
        title = task[3]
        due_date = task[4]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.configure(bg=UIStyle.COLORS["bg"])
        edit_window.resizable(False, False)

        lbl_title = tk.Label(edit_window)
        lbl_title.grid(row=0, column=0, padx=5, pady=5)
        UIStyle.apply_label_style(lbl_title, text="Title:", font="subheading")
        title_text = tk.Text(edit_window, height=1, width=40)
        title_text.grid(row=0, column=1, padx=5, pady=5)
        title_text.insert(tk.END, title)

        lbl_description = tk.Label(edit_window)
        lbl_description.grid(row=1, column=0, padx=5, pady=5)
        UIStyle.apply_label_style(lbl_description, text="Description:", font="subheading")
        description_text = tk.Text(edit_window, height=5, width=40)  # You can adjust height and width
        description_text.grid(row=1, column=1, padx=5, pady=5)
        description_text.insert(tk.END, description)

        lbl_priority = tk.Label(edit_window)
        lbl_priority.grid(row=2, column=0, padx=5, pady=5)
        UIStyle.apply_label_style(lbl_priority, text="Priority:", font="subheading")

        priority_var = tk.StringVar(value=priority)
        priority_dropdown = ttk.Combobox(edit_window, textvariable=priority_var,
                                         values=["Low", "Medium", "High", "Critical"], state="readonly")
        priority_dropdown.grid(row=2, column=1, padx=5, pady=5)

        btn_calendar_pull_up = tk.Button(edit_window)
        btn_calendar_pull_up.grid(row=3, column=0, padx=10, pady=5)
        UIStyle.apply_button_style(btn_calendar_pull_up, text="Select Due Date",
                                   command=lambda: PickDate.open_date_picker(self))

        self.date_label_task_created = tk.Label(edit_window)
        UIStyle.apply_label_style(self.date_label_task_created, text=f"Current: {due_date}", font="body")
        self.date_label_task_created.grid(row=3, column=1, padx=10)

        def save_changes():
            new_title = title_text.get("1.0", "end-1c").strip()
            new_priority = priority_var.get().strip()
            new_description = description_text.get("1.0", "end-1c").strip()
            date_value = self.date_label_task_created.cget("text").split(": ")[1]

            if new_title:
                self.object.db.UpdateTask(new_description, new_title, new_priority, date_value, task_id)
                messagebox.showinfo("Success", "Task updated successfully!")
                edit_window.destroy()
                self.show_tasks(self.object, self.frame)  # Refresh UI
                self.highlight_task_dates(self.object)
            else:
                messagebox.showerror("Fail", "Title was removed")

        save_btn = tk.Button(edit_window)
        save_btn.grid(row=4, column=0, columnspan=2, pady=10)
        UIStyle.apply_button_style(save_btn, text="Save Changes", command=save_changes, bg="primary")

    def delete_task(self, task):
        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            self.object.db.deleteTask(task[1])
            self.show_tasks(self.object, self.frame)
            self.highlight_task_dates(self.object)
            messagebox.showinfo("Success", "Task deleted successfully!")

    def go_back(self):
        print("Closing application...")
        self.master.destroy()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.task_canvas.yview_scroll(-1, "units")  # Scroll up
        else:
            self.task_canvas.yview_scroll(1, "units")  # Scroll down

# Run the Application
#root = tk.Tk()
#app = TaskCalendarApp(root)
#root.mainloop()
