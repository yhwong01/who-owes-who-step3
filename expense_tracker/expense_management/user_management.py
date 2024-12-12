import sqlite3

class UserNotFoundError(Exception):
    pass

class UserManager:
    def __init__(self, db):
        self.db = db

    def add_user(self, name,balance = 0):
        try:
            self.db.cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            #self.db.cursor.execute("INSERT OR IGNORE INTO balances (user, balance) VALUES (?, ?)", (name,balance,))
            self.db.conn.commit()
            return f"User '{name}' added successfully."
        except sqlite3.IntegrityError:
            return f"User '{name}' already exists."

    def remove_user(self, name):
        #added user defined exception
        try:
            self.db.cursor.execute("select FROM users WHERE name = ?", (name,))
            user = self.db.cursor.fetchone()
            if user is None:
                raise UserNotFoundError()

            self.db.cursor.execute("DELETE FROM users WHERE name = ?", (name,))
            #self.db.cursor.execute("DELETE FROM balances WHERE user = ?", (name,))
            self.db.conn.commit()
            return f"User '{name}' removed successfully."
        except UserNotFoundError:
            print("User not found")

    def list_users(self):
        self.db.cursor.execute("SELECT name FROM users")
        return [row[0] for row in self.db.cursor.fetchall()]