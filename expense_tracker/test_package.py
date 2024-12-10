from expense_management.db_management import DatabaseManager
from expense_management.user_management import UserManager
from expense_management.expense_operations import ExpenseManager
from reporting_tools.balance_calculation import BalanceManager
from reporting_tools.report_generation import ReportGeneration

# Initialize the database and managers
db = DatabaseManager("expense_tracker.db")
user_manager = UserManager(db)
expense_manager = ExpenseManager(db)
balance_manager = BalanceManager(db)
report_generator = ReportGeneration(db)

# Add sample users
print("Adding users...")
user_manager.add_user("Alice", 0)
user_manager.add_user("Bob", 0)
user_manager.add_user("Charlie", 0)

# Add expenses
print("Adding expenses...")
expense_manager.add_expense("Alice", 100, ["Alice", "Bob", "Charlie"])
expense_manager.add_expense("Bob", 50, ["Bob", "Charlie"])

# Display users
print("\nUsers:")
print(user_manager.list_users())

# Display expenses
print("\nExpenses:")
for expense in expense_manager.list_expenses():
    print(expense)

# Calculate balances and debts
print("\nCalculating balances...")
balance_manager.calculate_balances()

print("\nDebts:")
balance_manager.calculate_debts()

# Generate and export report
print("\nGenerating report...")
report = report_generator.generate_summary(format="text")
print(report)

report_generator.export_report(file_format="txt")

# Visualize debts
print("\nVisualizing debts...")
report_generator.visualize_debts(save_to_file=True)

# Cleanup
db.close()
