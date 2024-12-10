import unittest
from test_balance_calculation import TestBalanceCalculation
from test_report_generation import TestReportGeneration

# Create a test suite
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestBalanceCalculation))
    test_suite.addTest(unittest.makeSuite(TestReportGeneration))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
