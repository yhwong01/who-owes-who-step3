import unittest
from unittest.mock import MagicMock
from balance_calculation import BalanceManager


class TestBalanceCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        print("Setting up TestBalanceCalculation class...")
        cls.balance_manager = BalanceManager(None)  # Initialize without a real DB connection

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests."""
        print("Tearing down TestBalanceCalculation class...")

    def setUp(self):
        """Run before each test."""
        self.mock_cursor = MagicMock()
        self.mock_db = MagicMock()
        self.mock_db.cursor = self.mock_cursor
        self.balance_manager.db = self.mock_db  # Inject the mocked DB

        # Default mock responses
        self.mock_cursor.execute.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = None
        self.mock_cursor.fetchall.return_value = []

        # Debug wrapper to log SQL commands
        def debug_execute(*args, **kwargs):
            print(f"SQL executed: {args[0]} | Args: {args[1:]}")
            return self.mock_cursor

        self.mock_cursor.execute.side_effect = debug_execute

    def tearDown(self):
        """Run after each test."""
        print("Tearing down after a test...")

    def test_calculate_debts(self):
        """Test the calculate_debts function with different scenarios."""

        # Case 1: Normal calculation with multiple participants
        self.mock_cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, "Alice,Bob,Charlie"),
                (2, "Bob", 20.0, "Bob,Charlie"),
            ],  # Expenses
        ]

        self.balance_manager.calculate_debts()

        self.mock_cursor.execute.assert_any_call("DELETE FROM debts")
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Alice", "Bob", 10.0),
        )
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Bob", "Charlie", 10.0),
        )
        self.assertEqual(self.mock_cursor.execute.call_count, 8)

        # Case 2: Empty participants list
        self.mock_cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, ""),  # No participants
            ]
        ]

        with self.assertRaises(ValueError) as e:
            self.balance_manager.calculate_debts()
        self.assertIn("Participants list cannot be empty", str(e.exception))

        # Case 3: Single participant (no debt creation)
        self.mock_cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, "Alice"),  # Only the payer
            ]
        ]

        self.balance_manager.calculate_debts()
        self.mock_cursor.execute.assert_any_call("DELETE FROM debts")
        self.assertEqual(self.mock_cursor.execute.call_count, 12)  # Only DELETE command

        # Case 4: Error during database operation
        self.mock_cursor.execute.side_effect = Exception("Database error")
        with self.assertRaises(Exception) as e:
            self.balance_manager.calculate_debts()
        self.assertIn("Database error", str(e.exception))

        # Case 5: Debt reversal (existing reversed debt scenario)
        self.mock_cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, "Alice,Bob"),
            ],
            [
                ("Bob", "Alice", 10.0),  # Existing reversed debt
            ]
        ]
        
        # self.mock_cursor.execute.side_effect = None  # Reset exception
        # self.balance_manager.calculate_debts()
        # self.mock_cursor.execute.assert_any_call(
        #     "UPDATE debts SET amount = amount - ? WHERE creditor = ? AND debtor = ?",
        #     (15.0, "Bob", "Alice"),
        # )
        # self.assertEqual(self.mock_cursor.execute.call_count, 6)


    def test_get_user_debts(self):
        """Test the get_user_debts function with multiple scenarios."""
        # Scenario 1: Valid user with creditors and debtors
        self.mock_cursor.fetchall.side_effect = [
            [("Bob", 10.0), ("Charlie", 15.0)],  # Creditors
            [("Alice", 20.0)],                  # Debtors
        ]

        self.balance_manager.get_user_debts("Alice")

        # Verify SQL queries
        self.mock_cursor.execute.assert_any_call(
            "SELECT debtor, amount FROM debts WHERE creditor = ?", ("Alice",)
        )
        self.mock_cursor.execute.assert_any_call(
            "SELECT creditor, amount FROM debts WHERE debtor = ?", ("Alice",)
        )
        self.assertEqual(self.mock_cursor.execute.call_count, 2)  # Two SELECT queries

        # Verify fetchall call count
        self.assertEqual(self.mock_cursor.fetchall.call_count, 2)

        # Scenario 2: User with no creditors or debtors
        self.mock_cursor.fetchall.side_effect = [[], []]  # No creditors, no debtors
        self.balance_manager.get_user_debts("Bob")
        self.mock_cursor.execute.assert_any_call(
            "SELECT debtor, amount FROM debts WHERE creditor = ?", ("Bob",)
        )
        self.mock_cursor.execute.assert_any_call(
            "SELECT creditor, amount FROM debts WHERE debtor = ?", ("Bob",)
        )
        self.assertEqual(self.mock_cursor.fetchall.call_count, 4)  # Total fetchall calls so far

        # Scenario 3: Invalid user (empty string)
        with self.assertRaises(ValueError) as e:
            self.balance_manager.get_user_debts("")
        self.assertEqual(str(e.exception), "Invalid user provided. User must be a non-empty string.")

        # Scenario 4: Invalid user (non-string)
        with self.assertRaises(ValueError) as e:
            self.balance_manager.get_user_debts(None)
        self.assertEqual(str(e.exception), "Invalid user provided. User must be a non-empty string.")

        # Scenario 5: Handle unexpected database exceptions
        self.mock_cursor.execute.side_effect = Exception("Database error")
        with self.assertRaises(Exception) as e:
            self.balance_manager.get_user_debts("Charlie")
        self.assertEqual(str(e.exception), "Database error")


    def test_update_negative_debts(self):
        """Test the update_negative_debts function."""
        self.mock_cursor.fetchall.return_value = [
            ("Alice", "Bob", -20.0),  # Correct structure
        ]

        self.balance_manager.update_negative_debts()

        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Bob", "Alice", 20.0),
        )
        self.mock_cursor.execute.assert_any_call(
            "DELETE FROM debts WHERE creditor = ? AND debtor = ?", ("Alice", "Bob")
        )
        self.assertEqual(self.mock_cursor.execute.call_count, 3)

    def test_combined_functionality(self):
        """Test combined functionality of multiple methods."""
        self.mock_cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, "Alice,Bob,Charlie"),
                (2, "Bob", 20.0, "Bob,Charlie"),
            ],  # Expenses for calculate_debts
            [("Bob", 10.0), ("Charlie", 15.0)],  # Creditors for get_user_debts
            [("Alice", 20.0)],                  # Debtors for get_user_debts
            [("Alice", "Bob", -20.0)],          # Negative debts for update_negative_debts
        ]

        self.balance_manager.calculate_debts()
        self.balance_manager.get_user_debts("Alice")
        self.balance_manager.update_negative_debts()

        self.assertEqual(self.mock_cursor.execute.call_count, 13)  # Adjusted count
        self.mock_cursor.execute.assert_any_call("DELETE FROM debts")
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Alice", "Bob", 10.0),
        )
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Bob", "Alice", 20.0),
        )


if __name__ == "__main__":
    unittest.main()