import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Driver import Database_Driver
from CalendarPicker import PickDate
from Style import UIStyle


class TaskGallery:
    def __init__(self, parentFrame, parentObject):
        #super().__init__(parent)  # Initialize Frame within parent
        self.root = parentObject.root
        self.priority_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        self.db = Database_Driver()

        # Sorting Options
        self.sort_var = tk.StringVar(value="Due Date")  # Default sort by Due Date

        tk.Label(parentFrame, text="Sort By:", bg=UIStyle.COLORS["bg"], fg="white").pack(side=tk.LEFT, padx=5)

        sort_dropdown = ttk.Combobox(
            parentFrame,
            textvariable=self.sort_var,
            values=["Due Date", "Title", "Priority"],
            state="readonly",
            width=12
        )
        sort_dropdown.pack(side=tk.TOP, padx=5)
        sort_dropdown.bind("<<ComboboxSelected>>", lambda event: self.load_tasks())

        btn_back = tk.Button(parentFrame)
        UIStyle.apply_button_style(btn_back, text="🔙 Back", bg="danger", command=lambda: parentObject.show_frame("home"))
        btn_back.pack(side=tk.TOP, padx=5)

        # Create a Canvas
        self.canvas = tk.Canvas(parentFrame, bg=UIStyle.COLORS["bg"])
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add a Scrollbar
        scrollbar = ttk.Scrollbar(parentFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the Canvas
        self.task_frame = tk.Frame(self.canvas)

        # Add the new frame to a window inside the Canvas
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Load and display tasks
        self.load_tasks()

    def load_tasks(self):
        # Clear previous tasks
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Fetch tasks from SQLite sorted by Due Date
        tasks = self.db.GetTaskList("rmsack@svsu.edu", self.sort_var.get())
        if self.sort_var.get() == "Due Date":
            tasks = sorted(tasks, key=lambda x: datetime.strptime(x[4], "%m/%d/%y"))
        elif self.sort_var.get() == "Priority":
           tasks = sorted(tasks, key=lambda x: self.priority_order.get(x[0].capitalize(), 5))


        for task in tasks:
            priority = task[0]
            task_id = task[1]
            description = task[2]
            title = task[3]
            due_date = task[4]

            # Task Card
            task_card = tk.Frame(self.task_frame, bg=UIStyle.COLORS["bg"], padx=10, pady=5, relief="raised", borderwidth=2)
            task_card.pack(fill=tk.X, pady=5, padx=10)

            # Task Labels
            title_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(title_lbl,text=f"Task: {title}", font="heading")
            title_lbl.pack(anchor="w")

            description_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(description_lbl, text=f"Description: {description}", font="body")
            description_lbl.pack(anchor="w")

            date_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(date_lbl, f"Due: {due_date}", font="body")
            date_lbl.pack(anchor="w")

            priority_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(priority_lbl, text=f"Priority: {priority}", font="body")
            priority_lbl.pack(anchor="w")

            # Buttons (Edit & Delete)
            btn_frame = tk.Frame(task_card, bg=UIStyle.COLORS["bg"])
            btn_frame.pack(anchor="e", pady=5)

            edit_btn = tk.Button(btn_frame, text="Edit", command=lambda t=task: self.edit_task(t), bg="blue", fg="white")
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(btn_frame, text="Delete", command=lambda t=task_id: self.delete_task(t), bg="red", fg="white")
            delete_btn.pack(side=tk.LEFT, padx=5)

    def edit_task(self, task):
        priority = task[0]
        task_id = task[1]
        description = task[2]
        title = task[3]
        due_date = task[4]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")

        tk.Label(edit_window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        title_text = tk.Text(edit_window, height=1, width=40)
        title_text.grid(row=0, column=1, padx=5, pady=5)
        title_text.insert(tk.END, title)

        tk.Label(edit_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        description_text = tk.Text(edit_window, height=5, width=40)  # You can adjust height and width
        description_text.grid(row=1, column=1, padx=5, pady=5)
        description_text.insert(tk.END, description)

        tk.Label(edit_window, text="Priority:").grid(row=2, column=0, padx=5, pady=5)
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
                self.db.UpdateTask(new_description,new_title,new_priority,date_value,task_id)
                messagebox.showinfo("Success", "Task updated successfully!")
                edit_window.destroy()
                self.load_tasks()  # Refresh UI

        save_btn = tk.Button(edit_window, text="Save Changes", command=save_changes, bg="green", fg="white")
        save_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def delete_task(self, task_id):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if confirm:
            self.db.deleteTask(task_id)
            messagebox.showinfo("Deleted", "Task removed successfully!")
            self.load_tasks()  # Refresh UI

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")  # Scroll up
        else:
            self.canvas.yview_scroll(1, "units")  # Scroll down




# Run the App
#root = tk.Tk()
#app = TaskGallery(root)
#root.mainloop()