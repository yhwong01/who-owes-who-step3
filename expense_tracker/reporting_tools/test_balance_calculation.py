import unittest
from unittest.mock import MagicMock
from balance_calculation import BalanceManager


class TestBalanceCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.balance_manager = BalanceManager(None)  # Initialize without a real DB connection

    def setUp(self):
        """Run before each test."""
        # Mock the database and cursor
        self.mock_cursor = MagicMock()
        self.mock_db = MagicMock()
        self.mock_db.cursor = self.mock_cursor
        self.balance_manager.db = self.mock_db  # Inject the mocked DB

        # Default mock responses for calculate_debts and get_user_debts
        self.mock_cursor.execute.return_value = self.mock_cursor
        self.mock_cursor.fetchone.return_value = None  # Default for no existing debts
        self.mock_cursor.fetchall.return_value = []  # Default to empty list

    def test_calculate_debts(self):
        """Test the calculate_debts function."""
        # Mock expenses dataset
        self.mock_cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, "Alice,Bob,Charlie"),
                (2, "Bob", 20.0, "Bob,Charlie"),
            ],  # Expenses
        ]

        self.balance_manager.calculate_debts()

        # Verify that DELETE was executed
        self.mock_cursor.execute.assert_any_call("DELETE FROM debts")

        # Verify that INSERT statements were executed
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Alice", "Bob", 10.0),
        )
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Bob", "Charlie", 10.0),
        )

    def test_get_user_debts(self):
        """Test the get_user_debts function."""
        # Mock SELECT responses for creditors and debtors
        self.mock_cursor.fetchall.side_effect = [
            [("Bob", 10.0), ("Charlie", 15.0)],  # Creditors
            [("Alice", 20.0)],                  # Debtors
        ]

        self.balance_manager.get_user_debts("Alice")

        # Verify that SELECT queries were executed
        self.mock_cursor.execute.assert_any_call(
            "SELECT debtor, amount FROM debts WHERE creditor = ?", ("Alice",)
        )
        self.mock_cursor.execute.assert_any_call(
            "SELECT creditor, amount FROM debts WHERE debtor = ?", ("Alice",)
        )

    def test_update_negative_debts(self):
        """Test the update_negative_debts function."""
        # Mock negative debts dataset
        self.mock_cursor.fetchall.return_value = [
            ("Alice", "Bob", -20.0),  # Correct structure
        ]

        self.balance_manager.update_negative_debts()

        # Verify that INSERT and DELETE statements were executed
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
            ("Bob", "Alice", 20.0),
        )
        self.mock_cursor.execute.assert_any_call(
            "DELETE FROM debts WHERE creditor = ? AND debtor = ?", ("Alice", "Bob")
        )


if __name__ == "__main__":
    unittest.main()
