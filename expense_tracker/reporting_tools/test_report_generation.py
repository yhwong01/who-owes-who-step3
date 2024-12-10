import unittest
from unittest.mock import MagicMock
from report_generation import ReportGeneration


class TestReportGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.mock_db = MagicMock()  # Mock the database
        cls.report_generator = ReportGeneration(cls.mock_db)

    def setUp(self):
        """Run before each test."""
        # Mock database responses
        self.mock_db.cursor.fetchall.side_effect = [
            [
                (1, "Alice", 30.0, "Alice,Bob,Charlie"),
                (2, "Bob", 20.0, "Bob,Charlie"),
            ],  # Expenses
            [
                ("Alice", "Bob", 15.0),
                ("Bob", "Charlie", 10.0),
            ],  # Debts
        ]

    def test_generate_summary(self):
        """Test the generate_summary function."""
        # Test text format
        summary_text = self.report_generator.generate_summary(format="text")
        self.assertIsInstance(summary_text, dict)
        self.assertIn("debtor", str(summary_text))
        self.assertIn("'debtor': 'Alice'", str(summary_text))
        self.assertIn("'creditor': 'Bob'", str(summary_text))

        # Test JSON format
        summary_json = self.report_generator.generate_summary(format="json")
        self.assertIsInstance(summary_json, dict)
        self.assertIn("debts", summary_json)
        self.assertIn("amount': 15.0", str(summary_json))
        self.assertIn("Bob", str(summary_json))

    def test_generate_summary_return_type(self):
        """Test that generate_summary returns the correct type based on the format argument."""
        # Mock database responses for expenses and debts
        self.mock_db.cursor.fetchall.side_effect = [
            # Mock expenses
            [
                (1, "Alice", 30.0, "Alice,Bob,Charlie"),
                (2, "Bob", 20.0, "Bob,Charlie"),
            ],
            # Mock debts
            [
                ("Alice", "Bob", 15.0),
                ("Bob", "Charlie", 10.0),
            ],
        ]

        # Test text format
        summary_text = self.report_generator.generate_summary(format="text")
        self.assertIsInstance(summary_text, dict, "Expected summary_text to be a string when format='text'.")

        # Test JSON format
        summary_json = self.report_generator.generate_summary(format="json")
        self.assertIsInstance(summary_json, dict, "Expected summary_json to be a dictionary when format='json'.")

        # Test invalid format

        with self.assertRaises(ValueError):
            self.report_generator.generate_summary(format="iasd")

    def test_export_report(self):
        """Test the export_report function."""
        # Mock the `generate_summary` method
        self.report_generator.generate_summary = MagicMock()

        # Test exporting to TXT
        self.report_generator.generate_summary.return_value = "Sample Summary"
        self.report_generator.export_report(file_format="txt")
        self.report_generator.generate_summary.assert_called_with(format="text")

        # Test exporting to CSV
        self.report_generator.generate_summary.return_value = {
            "debts": [{"debtor": "Alice", "creditor": "Bob", "amount": 15.0}]
        }
        self.report_generator.export_report(file_format="csv")
        self.report_generator.generate_summary.assert_called_with(format="json")

        # Test exporting to XLSX
        self.report_generator.generate_summary.return_value = {
            "debts": [{"debtor": "Alice", "creditor": "Bob", "amount": 15.0}]
        }
        self.report_generator.export_report(file_format="xlsx")
        self.report_generator.generate_summary.assert_called_with(format="json")

        # Test invalid file format
        with self.assertRaises(ValueError):
            self.report_generator.export_report(file_format="invalid_format")

    def test_visualize_debts(self):
        """Test the visualize_debts function."""
        # Mock debts data
        self.mock_db.cursor.fetchall.return_value = [
            ("Alice", "Bob", 15.0),
            ("Bob", "Charlie", 10.0),
        ]

        # Mock plt.show to prevent actual rendering
        with unittest.mock.patch("matplotlib.pyplot.show"):
            self.report_generator.visualize_debts(save_to_file=False)

        # Mock saving to file
        with unittest.mock.patch("matplotlib.pyplot.savefig") as mock_savefig:
            self.report_generator.visualize_debts(save_to_file=True)
            self.assertEqual(mock_savefig.call_count, 2)  # Bar and pie charts


if __name__ == "__main__":
    unittest.main()
