import sqlite3

class DatabaseManager:
    def __init__(self, db_name="expense_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        # Expenses table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payer TEXT NOT NULL,
                amount REAL NOT NULL,
                participants TEXT NOT NULL,
                FOREIGN KEY (payer) REFERENCES users(name)
            )
        """)

        # Balances table (tracks net balances)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS balances (
                user TEXT PRIMARY KEY,
                balance REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (user) REFERENCES users(name)
            )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()
