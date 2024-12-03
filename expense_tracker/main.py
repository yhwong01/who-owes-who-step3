from expense_management.db_management import DatabaseManager
from expense_management.user_management import UserManager
from expense_management.expense_operations import ExpenseManager

#pending
#from reporting_tools.balance_calculation import BalanceCalculator
#from reporting_tools.report_generation import ReportGenerator

def add_user(user_manager):
    name = input("Enter the name of the user to add: ").strip()
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

def list_expenses(expense_manager):
    print("\nList of Expenses:")
    for expense in expense_manager.list_expenses():
        print(f"- ID: {expense[0]}, Payer: {expense[1]}, Amount: {expense[2]}, Participants: {expense[3]}")

def show_balances(balance_calculator):
    print("\nCurrent Balances:")
    balances = balance_calculator.calculate_balances()
    for user, balance in balances.items():
        print(f"{user}: {balance:.2f}")

def simplify_debts(balance_calculator):
    print("\nSuggested Debt Simplifications:")
    suggestions = balance_calculator.simplify_debts()
    for suggestion in suggestions:
        print(suggestion)

'''def generate_report(report_generator, balance_calculator):
    print("\nGenerating Report...")
    balances = balance_calculator.calculate_balances()
    report_generator.generate_summary(balances)
    format_choice = input("Enter report format (txt or csv): ").strip().lower()
    if format_choice in ["txt", "csv"]:
        report_generator.export_report(balances, format=format_choice)
        print(f"Report exported as {format_choice}.")
    else:
        print("Invalid format. Report generation canceled.")'''

'''def visualize_balances(report_generator, balance_calculator):
    print("\nVisualizing Balances...")
    balances = balance_calculator.calculate_balances()
    report_generator.visualize_balances(balances)'''

def settle_debts(expense_manager, balance_calculator):
    print("\nSettling debts...")
    transactions = expense_manager.settle_debt()
    for transaction in transactions:
        print(transaction)

    print("\nUpdated Balances:")
    show_balances(balance_calculator)

def main():
    # Initialize database and managers
    db = DatabaseManager(db_name="expense_tracker.db")
    user_manager = UserManager(db)
    expense_manager = ExpenseManager(db)
    #balance_calculator = BalanceCalculator(db)
    #report_generator = ReportGenerator()

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
        print("8. Visualize balances")
        print("9. Settle debts")
        print("10. Exit")

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
            show_balances(balance_calculator)
        elif choice == "6":
            simplify_debts(balance_calculator)
        elif choice == "7":
            pass
            #generate_report(report_generator, balance_calculator)
        elif choice == "8":
            pass
            #visualize_balances(report_generator, balance_calculator)
        elif choice == "9":
            settle_debts(expense_manager, balance_calculator)
        elif choice == "10":
            print("\n--- Thank you for using Expense Tracker! Goodbye! ---")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()
