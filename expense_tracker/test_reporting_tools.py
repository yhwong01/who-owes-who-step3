import sqlite3
from expense_management.db_management import DatabaseManager
from reporting_tools.balance_calculation import BalanceManager

def test_balance_manager():
    # Setup: Create an in-memory database for testing
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
        ],
    )
    db.conn.commit()

    # Test: Calculate debts
    balance_manager.calculate_debts()
    debts = db.cursor.execute("SELECT * FROM debts").fetchall()
    assert len(debts) == 4  # Check that all debts are recorded
    print("Debts after calculate_balances:", debts)

    # Test: Simplify debts
    balance_manager.simplify_debts()
    simplified_debts = db.cursor.execute("SELECT * FROM debts").fetchall()
    print("Debts after simplify_debts:", simplified_debts)

    # Test: Get user debts
    alice_debts = balance_manager.get_user_debts("Alice")
    print("Alice's debts:", alice_debts)

    bob_debts = balance_manager.get_user_debts("Bob")
    print("Bob's debts:", bob_debts)

    # Cleanup
    db.close()

# Run the test
test_balance_manager()
