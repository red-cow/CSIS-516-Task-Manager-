import os
import sys
import sqlite3
class Database_Driver:

    def __init__(self):
        if getattr(sys, 'frozen', False): #see's if this is running on the exe or in pychram
            # Running from PyInstaller bundle
            base_path = os.path.dirname(sys.executable) # exe
        else:
            # Running from source
            base_path = os.path.dirname(__file__) #pycharm

        db_path = os.path.join(base_path, "TaskManager.db") # makes the db path dynamic depending on environment
        self.conn = sqlite3.connect(db_path) # connects to db
        self.cursor = self.conn.cursor()
        self.create_tables_if_not_exist() #creates the table if this is the first instances of the db

    def create_tables_if_not_exist(self):
        # Create User table if it doesn't exist
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS User (
                    Email TEXT NOT NULL UNIQUE PRIMARY KEY,
                    Name TEXT NOT NULL,
                    "Date of Brith" DATE,
                    Password VARCHAR(30) NOT NULL CHECK (LENGTH(Password) >= 8)
                );
        """)

        # Create Task table if it doesn't exist
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Task (
                    Priority TEXT NOT NULL,
                     ID TEXT NOT NULL UNIQUE PRIMARY KEY,
                    Description TEXT,
                    Title TEXT NOT NULL,
                    "Due Date" DATE,
                    Email TEXT NOT NULL,
                    FOREIGN KEY (Email) REFERENCES User(Email)
                );
        """)
        self.conn.commit()

    def CreateTask(self, priority, description, title, due_date, email): # creates a task
        if not all([description.strip(), title.strip(), due_date.strip(), email.strip()]): # see's if any fields are empty
            print("Error: One or more fields are empty.")
            return False


        try:
            self.cursor.execute(
                "SELECT ID FROM Task WHERE Email = ? ORDER BY CAST(SUBSTR(ID, 1, INSTR(ID, '@') - 1) AS INTEGER) DESC LIMIT 1",
                (email,))
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
        # creates a new task object
        self.cursor.execute("INSERT INTO Task (Priority, ID, Description, Title, 'Due Date', Email) "
                            "VALUES (?, ?, ?, ?, ?, ?)"
                            ,(priority,id,description,title,due_date,email,))
        self.conn.commit()
        return True

    def deleteTask(self, id): # deletes a task
        self.cursor.execute("DELETE FROM Task WHERE ID = ?", (id,))
        self.conn.commit()

    def GetTaskSingle(self, id): # gets a task based on it's id
        if id.strip() == "":
            print("empty ID")
            return
        self.cursor.execute("SELECT * FROM Task WHERE ID = ?", (id,))
        results = self.cursor.fetchone()
        return results
    def GetTaskByDate(self, date, email): # gets a list of task to a given user sorted by date
        if date.strip() == "":
            print("empty date")
            return

        self.cursor.execute("""SELECT * FROM Task WHERE "Due Date" = ?  AND Email = ?""", (date, email))
        results = self.cursor.fetchall() # gets the list of task
        return results

    def HighlightTaskDate(self, email): # gets all distinct dates of a users tasks to give to there calendar
        self.cursor.execute("""SELECT DISTINCT "Due Date", Priority FROM Task WHERE "Due Date" IS NOT NULL AND Email = ?""", (email,) )
        return self.cursor.fetchall()

    def GetTaskList(self, email,sort_column="Due Date"): #gets a list of tasks from a given user but you can change the way they come sorted
        if email.strip() == "":
            print("no email provided")
            return []
        if sort_column == "Title": # if you want sorted by title
            self.cursor.execute( # is special because it needs to be lower case to work correctly in sql
                "SELECT * FROM Task WHERE Email = ? ORDER BY LOWER(Title) ASC",
                (email,)
            )
        else:
            self.cursor.execute( # any instance where you are not dealing with the title
                """SELECT * FROM Task 
                WHERE Email = ?
                """,
                (email,)
            )
        results = self.cursor.fetchall() # gets list from the database
        return results

    def UpdateTask(self, new_description, new_title, new_priority, new_date, task_id): # updates a given task
        with sqlite3.connect("TaskManager.db") as conn: # do to locking issues with updating we use a new temporay connection
            cursor = conn.cursor() # temp cursor
            cursor.execute( # update
                "UPDATE Task SET Title = ?, Priority = ?, Description = ?, 'Due Date' = ? WHERE ID = ?",
                (new_title, new_priority, new_description, new_date, task_id)
            )
            conn.commit() # a real commit to the database

            print("Task updated successfully") #temporay connection is closed


    def CreateUser(self, email, name, dob, password): # create a new user
        self.cursor.execute("INSERT INTO User (Email, Name, 'Date of Brith', Password) VALUES (?, ?, ?, ?)",
                            (email, name, dob, password))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM User WHERE Email = ?", (email,)) # gets me the newly created user
        return self.cursor.fetchone() # return the new created user
    def GetUser(self, email): # get a user based on there email
        self.cursor.execute("SELECT * FROM User WHERE Email = ?", (email,))
        return self.cursor.fetchone()

