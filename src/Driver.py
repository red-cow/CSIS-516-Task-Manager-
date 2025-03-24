import datetime
import sqlite3
class Database_Driver:

    def __init__(self):
        self.conn = sqlite3.connect("TaskManager.db")
        self.cursor = self.conn.cursor()

    def CreateTask(self, priority, description, title, due_date, email):
        if not all([priority.strip(), description.strip(), title.strip(), due_date.strip(), email.strip()]):
            print("Error: One or more fields are empty.")
            return
        try:
            self.cursor.execute("SELECT MAX(ID) FROM Task WHERE Email = ?", (email,))
            max_id = self.cursor.fetchone()[0]
            print(max_id)

            if max_id:
                numeric_part = ''.join(filter(str.isdigit, max_id))  # Get only the numeric part
                new_id_number = int(numeric_part) + 1  # Increment by 1
            else:
                new_id_number = 1  # Start with 1 if no tasks exist for this email

            id = f"{new_id_number}{email}"
            print(id)

        except Exception as e:
            print(e)
            id = "1" + email

        self.cursor.execute("INSERT INTO Task (Priority, ID, Description, Title, 'Due Date', Email) "
                            "VALUES (?, ?, ?, ?, ?, ?)"
                            ,(priority,id,description,title,due_date,email,))
        self.conn.commit()

    def deleteTask(self, id):
        self.cursor.execute("DELETE FROM Task WHERE ID = ?", (id,))
        self.conn.commit()

    def GetTaskSingle(self,id):
        if id.strip() == "":
            print("empty ID")
            return
        self.cursor.execute("SELECT * FROM Task WHERE ID = ?", (id,))
        results = self.cursor.fetchone()
        print(results)
        return results

    def GetTaskList(self, email):
        if email.strip() == "":
            print("no email provided")
            return []
        self.cursor.execute("SELECT * FROM Task WHERE Email = ?", (email,))
        results = self.cursor.fetchall()
        print(results)
        return results

    def CreateUser(self):
        pass
    def GetUser(self, email):
        self.cursor.execute("SELECT * FROM User WHERE Email = ?", (email,))
        return self.cursor.fetchone()


db = Database_Driver()
db.CreateTask("high","what's up","No way", "2025-04-10", "rmsack@svsu.edu")
db.GetTaskSingle("4rmsack@svsu.edu")
db.GetTaskList("rmsack@svsu.edu")