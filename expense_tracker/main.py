from expense_management.db_management import DatabaseManager
from expense_management.user_management import UserManager
from expense_management.expense_operations import ExpenseManager

from reporting_tools.balance_calculation import BalanceManager
from reporting_tools.report_generation import ReportGeneration

def add_user(user_manager):
    name = input("Enter the name of the user to add: ").strip()
    bal = float(input("Enter initial balance of the user: "))
    result = user_manager.add_user(name,bal)
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

"""def show_balances(balance_calculator):
    print("\nCurrent Balances: ")
    balances = balance_calculator.calculate_balances()"""


def show_debts(balance_calculator):
    print("\nCurrent Balances: ")
    balances = balance_calculator.calculate_balances()

def simplify_debts(balance_calculator):
    balance_calculator.simplify_debts()
    print("Debt Simplified :)")

def generate_report(report_generator, balance_calculator):
    print("\nGenerating Report...")
    #balances = balance_calculator.calculate_balances()
    format_choice = input("Enter report format ('text' or 'json'): ").strip().lower()
    if format_choice in ["text", "json"]:
        print(report_generator.generate_summary(format_choice))
    else:
        print("Invalid format. Report generation canceled.")

    """format_choice = input("Enter report format (txt or csv): ").strip().lower()
    if format_choice in ["txt", "csv"]:
        report_generator.export_report(balances, format=format_choice)
        print(f"Report exported as {format_choice}.")
    else:
        print("Invalid format. Report generation canceled.")"""
    return

def visualize_debts(report_generator, balance_calculator):
    print("\nVisualizing Balances...")
    #balances = balance_calculator.calculate_balances()
    report_generator.visualize_debts()

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
def export_report(report_generator, balance_calculator):
    format_choice = input("Enter report format (txt, csv, or xlsx): ").lower()
    if format_choice in ["txt","csv","xlsx"]:
        print(report_generator.export_report(format_choice))
    else:
        print("Invalid format. Report export canceled.")

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
        print("5. Show balances")
        print("6. Suggest debt simplifications")
        print("7. Generate a report")
        print("8. Visualize debts")
        print("9. Settle debts")
        print("10. Generate a report")
        print("11. Show user debts")
        print("12. Calculate debts")
        print("13. Exit")

        choice = input("Enter your choice (1-10): \n").strip()

        if choice == "1":
            add_user(user_manager)
        elif choice == "2":
            add_expense(expense_manager)
        elif choice == "3":
            list_users(user_manager)
        elif choice == "4":
            list_expenses(expense_manager)
        elif choice == "5":
            pass
            #show_debts(balance_manager)
            bal = db.cursor.execute("SELECT * FROM balances").fetchall()
            print("Balances:", bal )
        elif choice == "6":
            simplify_debts(balance_manager)
            debt = db.cursor.execute("SELECT * FROM debts").fetchall()
            print("Simplified Debts:", debt)
        elif choice == "7":
            generate_report(report_generator,balance_manager)
        elif choice == "8":
            visualize_debts(report_generator, balance_manager)
        elif choice == "9":
            settle_debts(expense_manager)
        elif choice == "10":
            generate_report(report_generator,balance_manager)
        elif choice == "11":
            user = input("Enter the name of the user to view debts: ")
            balance_manager.get_user_debts(user)
        elif choice == "12":
            balance_manager.calculate_debts()
        elif choice == "13":
            print("\n--- Thank you for using Expense Tracker! Goodbye! ---")
            break
        else:
            print("Invalid choice. Please try again.")
    db.close()

if __name__ == "__main__":
    main()
