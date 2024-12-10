from expense_tracker.reporting_tools.balance_calculation import BalanceManager
from expense_tracker.reporting_tools.report_generation import ReportGeneration     
from expense_tracker.expense_management.db_management import DatabaseManager

if __name__ == "__main__":

    db = DatabaseManager("expense_tracker.db")
    sample_expenses = [
        ("Alice", 60.0, "Alice,Bob,Charlie"),  # Alice pays for Bob and Charlie
        ("Dave", 30.0, "Dave,Alice"),          # Dave pays and includes Alice
        ("Alice", 50.0, "Alice,Eve"),          # Alice pays for Eve
        ("Frank", 100.0, "Frank,Alice"),       # Frank pays for Alice
        ("George", 80.0, "George,Alice"),      # George pays for Alice
        ("Alice", 20.0, "Alice,Hannah"),       # Alice pays for Hannah
    ]

    # Insert these expenses into the `expenses` table
    for payer, amount, participants in sample_expenses:
        db.cursor.execute(
            "INSERT INTO expenses (payer, amount, participants) VALUES (?, ?, ?)",
            (payer, amount, participants),
        )

    balance_manager = BalanceManager(db)
    balance_manager.calculate_debts()

    new = db.cursor.execute("SELECT * FROM debts").fetchall()
    print("Debts after calculation:", new)

    db.conn.commit()

    report_gen = ReportGeneration(db)
    print("Before calling visualize_simple_debt_summary")
    report_gen.visualize_balances("Alice")
    print("After calling visualize_simple_debt_summary")