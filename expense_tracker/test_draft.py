import sqlite3
from expense_management.db_management import DatabaseManager
from reporting_tools.balance_calculation import BalanceManager


db = DatabaseManager(":memory:")  # Use in-memory SQLite for testing
balance_manager = BalanceManager(db)

# Add sample users and expenses
db.cursor.executemany(
    "INSERT INTO users (name) VALUES (?)", [("Alice",), ("Bob",), ("Charlie",)]
)
db.cursor.executemany(
    """
    INSERT INTO expenses (payer, amount, participants) 
    VALUES (?, ?, ?)
    """,
    [
        ("Alice", 30, "Alice,Bob,Charlie"),  # Alice pays 30, split with Bob and Charlie
        ("Bob", 20, "Bob,Charlie"),          # Bob pays 20, split with Charlie
        ("Bob", 5, "Alice,Bob"),              # Check for update on existing debt relationship
        ("Charlie", 25, "Alice,Charlie"),    # New: Charlie pays 25, split with Alice
        ("Alice", 15, "Alice,Bob"),          # New: Alice pays 15, split with Bob
        ("Charlie", 20, "Bob,Charlie"),      # New: Charlie pays 20, split with Bob
        ("Bob", 30, "Alice,Charlie"),        # New: Bob pays 30, split with Alice and Charlie
        ("Alice", 40, "Bob,Charlie"),        # New: Alice pays 40, split with Bob and Charlie
        ("Charlie", 50, "Alice,Bob")         # New: Charlie pays 50, split with Alice and Bob
    ],
)
db.conn.commit()

expenses = db.cursor.execute("SELECT * FROM expenses").fetchall()
print(expenses)

# Test: Calculate debts
balance_manager.calculate_debts()
debts = db.cursor.execute("SELECT * FROM debts").fetchall()
assert len(debts) == 3  # Check that all debts are recorded
print(debts)

# Test: update negative debts
balance_manager.update_negative_debts()
new_debts = db.cursor.execute("SELECT * FROM debts").fetchall()
print(new_debts)

# Test: get_user_debts
alice_debts = balance_manager.get_user_debts("Alice")
alice_debts

bob_debts = balance_manager.get_user_debts("Bob")
bob_debts

