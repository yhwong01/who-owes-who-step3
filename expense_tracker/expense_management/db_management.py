import sqlite3

class DatabaseManager:
    def __init__(self, db_name="./who-owes-who/expense_tracker/expense_tracker.db"):
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

        # Calculate and store the detailed debts between specific creditors and debtors for all recorded expenses
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creditor TEXT NOT NULL,
                debtor TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (creditor) REFERENCES users(name),
                FOREIGN KEY (debtor) REFERENCES users(name)
            )
        """)

        self.conn.commit()

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