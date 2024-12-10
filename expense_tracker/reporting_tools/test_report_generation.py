import unittest
from report_generation import ReportGenerator  # Import the module to test

class TestReportGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.report_generator = ReportGenerator(None)  # Pass a mock or stub database

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests."""
        cls.report_generator = None

    def setUp(self):
        """Run before each test."""
        self.sample_report_data = {
            "users": ["Alice", "Bob", "Charlie"],
            "balances": {"Alice": 10.0, "Bob": -15.0, "Charlie": 5.0},
        }

    def tearDown(self):
        """Run after each test."""
        self.sample_report_data = None

    def test_generate_report(self):
        """Test the generate_report function."""
        report = self.report_generator.generate_report(self.sample_report_data)
        self.assertIsInstance(report, str)
        self.assertIn("Alice", report)
        self.assertIn("Charlie", report)
        self.assertGreater(len(report), 0)

    def test_export_to_file(self):
        """Test the export_to_file function."""
        success = self.report_generator.export_to_file("test_report.txt")
        self.assertTrue(success)
        self.assertIsInstance(success, bool)
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
