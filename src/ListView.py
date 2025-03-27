import tkinter as tk
from tkinter import ttk, messagebox
from Driver import Database_Driver
import sqlite3


class TaskGallery:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Gallery")
        self.db = Database_Driver()

        # Database Connection
        self.conn = sqlite3.connect("TaskManager.db")
        self.cursor = self.conn.cursor()

        # Create a main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create a Canvas
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add a Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the Canvas
        self.task_frame = tk.Frame(self.canvas)

        # Add the new frame to a window inside the Canvas
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        # Load and display tasks
        self.load_tasks()

    def load_tasks(self):
        """Fetch and display tasks sorted by Due Date."""
        # Clear previous tasks
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Fetch tasks from SQLite sorted by Due Date
        tasks = self.db.GetTaskList("rmsack@svsu.edu")

        print(tasks)

        for task in tasks:
            priority = task[0]
            task_id = task[1]
            description = task[2]
            title = task[3]
            due_date = task[4]

            # Task Card
            task_card = tk.Frame(self.task_frame, bg="lightgray", padx=10, pady=5, relief="raised", borderwidth=2)
            task_card.pack(fill=tk.X, pady=5, padx=10)

            # Task Labels
            title_lbl = tk.Label(task_card, text=f"Task: {title}", font=("Arial", 12, "bold"), bg="lightgray")
            title_lbl.pack(anchor="w")

            description_lbl = tk.Label(task_card, text=f"Description: {description}", font=("Arial", 8 ), bg="lightgray" )
            description_lbl.pack(anchor="w")

            date_lbl = tk.Label(task_card, text=f"Due: {due_date}", font=("Arial", 10), bg="lightgray")
            date_lbl.pack(anchor="w")

            priority_lbl = tk.Label(task_card, text=f"Priority: {priority}", font=("Arial", 10), bg="lightgray")
            priority_lbl.pack(anchor="w")

            # Buttons (Edit & Delete)
            btn_frame = tk.Frame(task_card, bg="lightgray")
            btn_frame.pack(anchor="e", pady=5)

            edit_btn = tk.Button(btn_frame, text="Edit", command=lambda t=task: self.edit_task(t), bg="blue",
                                 fg="white")
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(btn_frame, text="Delete", command=lambda t=task_id: self.delete_task(t), bg="red",
                                   fg="white")
            delete_btn.pack(side=tk.LEFT, padx=5)

    def edit_task(self, task):
        """Open a window to edit a task."""
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

        def save_changes():
            new_title = title_text.get().strip()
            new_priority = priority_var.get().strip()
            new_description = description_text.get().strip()

            if new_title:
                self.cursor.execute("UPDATE Task SET Title = ?, Priority = ? WHERE ID = ?",
                                    (new_title, new_priority, task_id))
                self.conn.commit()
                messagebox.showinfo("Success", "Task updated successfully!")
                edit_window.destroy()
                self.load_tasks()  # Refresh UI

        save_btn = tk.Button(edit_window, text="Save Changes", command=save_changes, bg="green", fg="white")
        save_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def delete_task(self, task_id):
        """Delete a task from the database."""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if confirm:
            self.cursor.execute("DELETE FROM Task WHERE ID = ?", (task_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Task removed successfully!")
            self.load_tasks()  # Refresh UI


# Run the App
root = tk.Tk()
app = TaskGallery(root)
root.mainloop()