import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from CalendarPicker import PickDate
from Style import UIStyle


class TaskGallery:
    def main(self, parentFrame, parentObject):
        self.root = parentObject.root
        self.object = parentObject
        self.priority_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}

        lbl_title = tk.Label(parentFrame)
        lbl_title.grid(row=0, column=1, padx=10, pady=5, stick="w")
        UIStyle.apply_label_style(lbl_title, text="Look at Your tasks")

        lbl_sort_by = tk.Label(parentFrame)
        lbl_sort_by.grid(row=0, column=1, padx=10, pady=5, stick="e")
        UIStyle.apply_label_style(lbl_sort_by, text="Sort By:", font="body")

        # Sorting Options
        self.sort_var = tk.StringVar(value="Due Date")  # Default sort by Due Date

        sort_dropdown = ttk.Combobox(
            parentFrame,
            textvariable=self.sort_var,
            values=["Due Date", "Title", "Priority"],
            state="readonly",
            width=12
        )

        print("Selected:", self.sort_var.get())  # Should be "Due Date"

        sort_dropdown.grid(row=0, column=2, pady=5)
        # UIStyle.apply_combobox_style(sort_dropdown, self.sort_var, bg="neutral")
        sort_dropdown.bind("<<ComboboxSelected>>", lambda event: self.load_tasks())

        btn_cal = tk.Button(parentFrame)
        UIStyle.apply_button_style(btn_cal, text="📅 Cal View", command=lambda: parentObject.show_frame("calendar"))
        btn_cal.grid(row=0, column=3, padx=10, pady=5, sticky='e')

        btn_back = tk.Button(parentFrame)
        UIStyle.apply_button_style(btn_back, text="🔙 Home", bg="danger",
                                   command=lambda: parentObject.show_frame("home"))
        btn_back.grid(row=0, column=4, columnspan=2, padx=30, pady=5, sticky='e')

        parentFrame.grid_rowconfigure(1, weight=1)
        parentFrame.grid_columnconfigure(0, weight=1)

        # Canvas and Scrollbar Frame
        display_frame = tk.Frame(parentFrame, bg=UIStyle.COLORS["bg"])
        display_frame.grid(row=1, column=0, columnspan=5, rowspan=10, sticky="nsew")

        # Let display_frame's internal row/column grow too
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        # Configure weights for dynamic resizing
        parentFrame.grid_rowconfigure(1, weight=1)
        parentFrame.grid_columnconfigure(1, weight=1)

        # Create Canvas
        self.canvas = tk.Canvas(display_frame, bg=UIStyle.COLORS["bg"])
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5, sticky="nsew")

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=0, column=6, sticky="ns")

        # Configure Canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        #self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        # Create another frame inside the Canvas
        self.task_frame = tk.Frame(self.canvas, bg=UIStyle.COLORS["bg"])
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.task_frame.bind("<Configure>", on_frame_configure)

        # Scroll support
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Load and display tasks
        self.load_tasks()
    def __init__(self, parentFrame, parentObject):
        self.main(parentFrame, parentObject)


    def load_tasks(self):
        # Clear previous tasks
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Fetch tasks from SQLite sorted by Due Date
        tasks = self.object.db.GetTaskList(self.object.user[0], self.sort_var.get())
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
            task_card.pack(fill=tk.X, pady=5, padx=50)

            # Task Labels
            title_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(title_lbl,text=f"Task: {title}", font="heading", max_width=800)
            title_lbl.pack(anchor="w")

            description_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(description_lbl, text=f"Description: {description}", font="body", max_width=800)
            description_lbl.pack(anchor="w")

            date_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(date_lbl, f"Due: {due_date}", font="body")
            date_lbl.pack(anchor="w")

            priority_lbl = tk.Label(task_card)
            UIStyle.apply_label_style(priority_lbl, text=f"Priority: {priority}", font="body")
            priority_lbl.pack(anchor="w")

            btn_frame = tk.Frame(task_card, bg=UIStyle.COLORS["bg"])
            btn_frame.pack(anchor="e", pady=5)

            edit_btn = tk.Button(btn_frame)
            UIStyle.apply_button_style(edit_btn,text="Edit", command=lambda t=task: self.edit_task(t), bg="primary")
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(btn_frame)
            UIStyle.apply_button_style(delete_btn, text="Delete", command=lambda t=task_id: self.delete_task(t), bg="danger")
            delete_btn.pack(side=tk.LEFT, padx=5)

    def edit_task(self, task):
        priority = task[0]
        task_id = task[1]
        description = task[2]
        title = task[3]
        due_date = task[4]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.configure(bg=UIStyle.COLORS["bg"])
        edit_window.resizable(False,False)

        lbl_title = tk.Label(edit_window)
        lbl_title.grid(row=0, column=0, padx=5, pady=5)
        UIStyle.apply_label_style(lbl_title,text="Title:",font="subheading")
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
                self.object.db.UpdateTask(new_description,new_title,new_priority,date_value,task_id)
                messagebox.showinfo("Success", "Task updated successfully!")
                edit_window.destroy()
                self.load_tasks()  # Refresh UI
            else:
                messagebox.showerror("Fail", "Title was removed")

        save_btn = tk.Button(edit_window)
        save_btn.grid(row=4, column=0, columnspan=2, pady=10)
        UIStyle.apply_button_style(save_btn,text="Save Changes", command=save_changes, bg="primary")

    def delete_task(self, task_id):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if confirm:
            self.object.db.deleteTask(task_id)
            messagebox.showinfo("Deleted", "Task removed successfully!")
            self.load_tasks()  # Refresh UI

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")  # Scroll up
        else:
            self.canvas.yview_scroll(1, "units")  # Scroll down
