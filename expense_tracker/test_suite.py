import unittest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
print(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)

# Add subdirectories to the Python path if necessary
sys.path.append(os.path.join(PROJECT_ROOT, "expense_tracker"))

PARENT_DIR = os.path.dirname(__file__)
sys.path.append(PARENT_DIR)

# Add the directory to the Python path, to eliminate import errors
TEST_DIR = os.path.join(PARENT_DIR, "expense_management")
sys.path.append(TEST_DIR)
TEST_DIR = os.path.join(PARENT_DIR, "reporting_tools")
sys.path.append(TEST_DIR)

from expense_management.test_expense_manager import TestExpenseManager
from expense_management.test_manager import TestManager
from expense_management.test_user_manager import TestUserManager
from reporting_tools.test_balance_calculation import TestBalanceCalculation
from reporting_tools.test_report_generation import TestReportGeneration


def suite():
    suite = unittest.TestSuite()

    suite.addTest(TestExpenseManager('test_add_expense'))
    suite.addTest(TestExpenseManager('test_remove_expense'))
    suite.addTest(TestExpenseManager('test_list_expenses'))
    suite.addTest(TestExpenseManager('test_settle_debt'))

    suite.addTest(TestManager('test_manager_name'))
    suite.addTest(TestManager('test_str_method'))

    suite.addTest(TestUserManager('test_add_user'))
    suite.addTest(TestUserManager('test_remove_user'))
    suite.addTest(TestUserManager('test_list_users'))

    # Add tests from TestBalanceCalculation
    suite.addTest(TestBalanceCalculation('test_calculate_debts'))
    suite.addTest(TestBalanceCalculation('test_get_user_debts'))
    suite.addTest(TestBalanceCalculation('test_update_negative_debts'))
    suite.addTest(TestBalanceCalculation('test_combined_functionality'))

    # Add tests from TestReportGeneration
    suite.addTest(TestReportGeneration('test_generate_summary'))
    suite.addTest(TestReportGeneration('test_export_report'))
    suite.addTest(TestReportGeneration('test_visualize_balances'))

    return suite

if __name__ == "__main__":
    test_suite = suite()
    result = unittest.TestResult()
    print("Running Test Suite...")
    test_suite.run(result)

    print("\n--- Test Results ---")
    print(f"Tests Run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")

    #print errors
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"{test}: {traceback}")
        exit(1)

    #print failures
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"{test}: {traceback}")
        exit(1)

