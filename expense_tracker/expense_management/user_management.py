import sqlite3
class UserManager:
    def __init__(self, db):
        self.db = db

    def add_user(self, name):
        try:
            self.db.cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            self.db.cursor.execute("INSERT OR IGNORE INTO balances (user, balance) VALUES (?, 0)", (name,))
            self.db.conn.commit()
            return f"User '{name}' added successfully."
        except sqlite3.IntegrityError:
            return f"User '{name}' already exists."

    def remove_user(self, name):
        self.db.cursor.execute("DELETE FROM users WHERE name = ?", (name,))
        self.db.cursor.execute("DELETE FROM balances WHERE user = ?", (name,))
        self.db.conn.commit()
        return f"User '{name}' removed successfully."

    def list_users(self):
        self.db.cursor.execute("SELECT name FROM users")
        return [row[0] for row in self.db.cursor.fetchall()]
