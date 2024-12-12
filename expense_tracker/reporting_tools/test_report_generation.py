import unittest
import os
import glob
from unittest.mock import MagicMock, patch
from expense_tracker.reporting_tools.report_generation import ReportGeneration
from expense_tracker.expense_management.db_management import DatabaseManager
from expense_tracker.reporting_tools.balance_calculation import BalanceManager
from expense_tracker.reporting_tools.report_generation import ReportGeneration
import matplotlib.pyplot as plt


class TestReportGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        print("Setting up TestReportGeneration class...")
        cls.mock_db = MagicMock()  # Mock the database
        cls.report_generator = ReportGeneration(cls.mock_db)  # Initialize with mocked DB

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests."""
        print("Tearing down TestReportGeneration class...")

    def setUp(self):
        """Run before each test."""
        # Set up fresh mocked database responses for each test
        self.mock_db.cursor.fetchall.side_effect = [
            # Mock expenses
            [
                (1, "Alice", 30.00, "Alice,Bob,Charlie"),
                (3, "Alice", 50.00, "Alice,Bob"),
            ],
            # Mock debts
            [
                ("Alice", "Bob", 10.00),
                ("Charlie", "Alice", 15.00),
            ],
        ]
        print("Setting up for a test...")

    def tearDown(self):
        """Run after each test."""
        print("Tearing down after a test...")

    def test_generate_summary(self):
        """Test generate_summary for a specific user."""
        # Generate summary for Alice
        summary = self.report_generator.generate_summary("Alice")
        
        # Assertions
        self.assertIn("Expense Report for Alice", summary)
        self.assertIn("Payer: Alice, Amount: $30.00", summary)
        self.assertIn("You owe Bob: $10.00", summary)
        self.assertIn("Charlie owes you: $15.00", summary)
        self.assertIn("Total Amount You Owe: $10.00", summary)
        self.assertIn("Total Amount Owed to You: $15.00", summary)

    def test_export_report(self):
        """Test the export_report function."""
        # Mock the generate_summary method
        self.report_generator.generate_summary = MagicMock(
            return_value="""
            ### Expense Report for Alice (Generated on 2024-12-10 12:00:00):
            
            **Expense History:**
            - Payer: Alice, Amount: $30.00, Participants: Alice,Bob,Charlie
            - Payer: Alice, Amount: $50.00, Participants: Alice,Bob
            
            **Debt Situation:**
            - You owe Bob: $10.00
            - Charlie owes you: $15.00
            
            **Summary:**
            - Total Amount You Owe: $10.00
            - Total Amount Owed to You: $15.00
            """
        )

        # Test exporting as TXT
        self.report_generator.export_report("Alice", file_format="txt")
        txt_files = glob.glob("Alice_expense_report_*.txt")
        self.assertTrue(len(txt_files) > 0, "TXT file not generated.")
        self.assertTrue(any("Alice_expense_report" in f for f in txt_files), "TXT file does not match expected format.")

        # Test exporting as CSV
        self.report_generator.export_report("Alice", file_format="csv")
        csv_files = glob.glob("Alice_expense_report_*.csv")
        self.assertTrue(len(csv_files) > 0, "CSV file not generated.")
        self.assertTrue(any("Alice_expense_report" in f for f in csv_files), "CSV file does not match expected format.")

        # Test exporting as XLSX
        self.report_generator.export_report("Alice", file_format="xlsx")
        xlsx_files = glob.glob("Alice_expense_report_*.xlsx")
        self.assertTrue(len(xlsx_files) > 0, "XLSX file not generated.")
        self.assertTrue(any("Alice_expense_report" in f for f in xlsx_files), "XLSX file does not match expected format.")

        # Test invalid file format
        with self.assertRaises(ValueError):
            self.report_generator.export_report("Alice", file_format="invalid_format")

        # Cleanup generated files
        for file in txt_files + csv_files + xlsx_files:
            os.remove(file)

    @classmethod
    def visualize_balances(cls, db, current_user):
        """
        Generate a bar plot of the user's debt/credit balance using matplotlib.
        """
        # Fetch debts to compute visualization data for balances
        result = db.cursor.execute(
            "SELECT debtor, creditor, amount FROM debts WHERE debtor = ? OR creditor = ?",
            (current_user, current_user)
        ).fetchall()

        # Organize data for plotting
        balance_summary = {}
        for debtor, creditor, amount in result:
            if debtor == current_user:
                balance_summary[creditor] = balance_summary.get(creditor, 0) + amount
            elif creditor == current_user:
                balance_summary[debtor] = balance_summary.get(debtor, 0) - amount

        # Plotting
        names = list(balance_summary.keys())
        balances = list(balance_summary.values())

        plt.figure(figsize=(10, 6))
        plt.bar(names, balances, color='orange')
        plt.xlabel("People")
        plt.ylabel("Net Balance")
        plt.title(f"Debt Summary for {current_user}")
        plt.grid(axis='y', linestyle="--", alpha=0.7)
        plt.show()

    @classmethod
    def initialize_db(cls, db):
        """
        Ensure required tables exist in the database.
        """
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payer TEXT,
                amount FLOAT,
                participants TEXT
            );
        """)

        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                debtor TEXT,
                creditor TEXT,
                amount FLOAT
            );
        """)

        db.conn.commit()

    def test_visualize_balances(self):
        """
        Main test function to visualize Alice's balances and run simple assertions.
        """
        # Set up database connection
        db = DatabaseManager("expense_tracker.db")
        self.initialize_db(db)

        # Input sample expenses
        sample_expenses = [
            ("Alice", 60.0, "Alice,Bob,Charlie"),
            ("Dave", 30.0, "Dave,Alice"),
            ("Alice", 50.0, "Alice,Eve"),
            ("Frank", 100.0, "Frank,Alice"),
            ("George", 80.0, "George,Alice"),
            ("Alice", 20.0, "Alice,Hannah"),
        ]

        # Insert these expenses into database
        for payer, amount, participants in sample_expenses:
            db.cursor.execute(
                "INSERT INTO expenses (payer, amount, participants) VALUES (?, ?, ?)",
                (payer, amount, participants)
            )

        # Perform debt calculation
        balance_manager = BalanceManager(db)
        balance_manager.calculate_debts()
        db.conn.commit()

        # Fetch debts after calculation
        debts = db.cursor.execute("SELECT * FROM debts").fetchall()
        print("Debts after calculation:", debts)

        # Perform visualization
        self.visualize_balances(db, "Alice")

        # Test if there is valid debt entries
        assert len(debts) > 0, "There should be debt entries calculated."

        alice_debts = [d for d in debts if d[0] == "Alice"]

        # Test that Alice has valid debt entries
        total_debt_alice = sum(d[2] for d in alice_debts)  # Sum up debt amounts
        assert total_debt_alice >= 0, "Debt balances must be valid numbers."
        
        # Test to ensure that the debt amounts are positive
        assert all(d[2] > 0 for d in alice_debts), "All Alice's debt amounts should be greater than 0."

        # Test duplicates
        unique_debts = {(d[0], d[1], d[2]) for d in debts} 
        assert len(unique_debts) == len(debts), "Debt entries should not have duplicates for Alice."
        
        # Test if debts are fetched as a valid list from the database
        assert isinstance(debts, list), "Debts should be retrieved as a list from the database."
        db.close()
if __name__ == "__main__":
    unittest.main()
