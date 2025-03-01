import sqlite3
class Database_Driver:
    def Driver(self):
        self.conn = sqlite3.connect("TaskManager.db")
        self.cursor = self.conn.cursor()