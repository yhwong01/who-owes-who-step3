from expense_management.db_management import DatabaseManager
from expense_management.user_management import UserManager
from expense_management.expense_operations import ExpenseManager

from reporting_tools.balance_calculation import BalanceManager
from expense_tracker.reporting_tools.report_generation import ReportGeneration

def add_user(user_manager):
    name = input("Enter the name of the user to add: ").strip()
    #bal = float(input("Enter initial balance of the user: "))
    result = user_manager.add_user(name)
    print(result)


def add_expense(expense_manager):
    payer = input("Enter the name of the payer: ").strip()
    amount = float(input("Enter the expense amount: ").strip())
    participants = input("Enter the names of participants (comma-separated): ").strip().split(",")
    participants = [p.strip() for p in participants]
    result = expense_manager.add_expense(payer, amount, participants)
    print(result)

def list_users(user_manager):
    print("\nList of Users:")
    for user in user_manager.list_users():
        print(f"- {user}")
    print(f'Total number of Users: {len(user_manager.list_users())}')
def list_expenses(expense_manager):
    print("\nList of Expenses:")
    for expense in expense_manager.list_expenses():
        print(f"- ID: {expense[0]}, Payer: {expense[1]}, Amount: {expense[2]}, Participants: {expense[3]}")

def simplify_debts(balance_calculator):
    balance_calculator.simplify_debts()
    print("Debt Simplified :)")

def generate_report(report_generator):
    print("\nGenerating Report...")
    #balances = balance_calculator.calculate_balances()
    user_choice = input("Enter user name: ").strip().lower()
    print(report_generator.generate_summary(user_choice))

    """format_choice = input("Enter report format (txt or csv): ").strip().lower()
    if format_choice in ["txt", "csv"]:
        report_generator.export_report(balances, format=format_choice)
        print(f"Report exported as {format_choice}.")
    else:
        print("Invalid format. Report generation canceled.")"""
    return

def visualize_debts(report_generator):
    print("\nVisualizing Balances...")
    #balances = balance_calculator.calculate_balances()
    user = input("Enter the name of the user to show his/her balance: ").strip()
    report_generator.visualize_balances(user)

def settle_debts(expense_manager):
    print("\n--- Settle a Debt ---")
    payer = input("Enter the name of the payer: ").strip()
    receiver = input("Enter the name of the receiver: ").strip()
    try:
        amount = float(input("Enter the amount to settle: "))
        if amount <= 0:
            print("Amount must be a positive number.")
            return

        # Call the updated settle_debt method
        expense_manager.settle_debt(payer, receiver, amount)
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")
def export_report(report_generator):
    format_choice = input("Enter report format (txt, csv, or xlsx): ").lower()
    if format_choice in ["txt","csv","xlsx"]:
        print(report_generator.export_report(format_choice))
    else:
        print("Invalid format. Report export canceled.")

def remove_user(user_manager):
    name = input("Enter the name of the user to remove: ").strip()
    result = user_manager.remove_user(name)
    print(result)

def remove_expense(expense_manager):
    expense_id = input("Enter the id of the expense to remove: ").strip()
    result = expense_manager.remove_expense(expense_id)
    print(result)


def main():
    # Initialize database and managers
    db = DatabaseManager(db_name="expense_tracker.db")
    user_manager = UserManager(db)
    expense_manager = ExpenseManager(db)
    balance_manager = BalanceManager(db)
    report_generator = ReportGeneration(db)

    print("\n--- Welcome to Expense Tracker :) ---")
    while True:
        print("\nPlease choose an option:")
        print("1. Add a new user")
        print("2. Add a new expense")
        print("3. List all users")
        print("4. List all expenses")
        print("5. Remove a user")
        print("6. Remove Expense")
        print("7. Generate a report")
        print("8. Visualize debts")
        print("9. Settle debts")
        print("10. Calculate debts")
        print("11. Show user debts")
        print("12. Exit")
        #remove expense

        choice = input("Enter your choice (1-12): \n").strip()

        if choice == "1":
            add_user(user_manager)
        elif choice == "2":
            add_expense(expense_manager)
        elif choice == "3":
            list_users(user_manager)
        elif choice == "4":
            list_expenses(expense_manager)
        elif choice == "5":
            remove_user(user_manager)
        elif choice == "6":
            remove_expense(expense_manager)
        elif choice == "7":
            generate_report(report_generator)
        elif choice == "8":
            visualize_debts(report_generator)
        elif choice == "9":
            settle_debts(expense_manager)
        elif choice == "10":
            balance_manager.calculate_debts()
        elif choice == "11":
            user = input("Enter the name of the user to view debts: ")
            balance_manager.get_user_debts(user)
        elif choice == "12":
            print("\n--- Thank you for using Expense Tracker! Goodbye! ---")
            break
        else:
            print("Invalid choice. Please try again.")
        balance_manager.update_negative_debts()
    db.close()

if __name__ == "__main__":
    main()
