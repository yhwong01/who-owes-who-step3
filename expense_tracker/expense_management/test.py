from db_management import DatabaseManager
from user_management import UserManager
from expense_operations import ExpenseManager
##from balance_calculation import BalanceCalculator

# Initialize the database and managers
db = DatabaseManager()
user_manager = UserManager(db)
expense_manager = ExpenseManager(db)
#balance_calculator = BalanceCalculator(db)


# Function to add sample data
def add_sample_data():
    print("Adding sample users...")
    print(user_manager.add_user("Alice"))
    print(user_manager.add_user("Bob"))
    print(user_manager.add_user("Charlie"))
    print(user_manager.add_user("David"))

    print("\nAdding sample expenses...")
    print(expense_manager.add_expense("Alice", 100, ["Alice", "Bob", "Charlie"]))
    print(expense_manager.add_expense("Bob", 50, ["Bob", "Charlie"]))
    print(expense_manager.add_expense("Charlie", 75, ["Charlie", "Alice", "David"]))
    print(expense_manager.add_expense("David", 40, ["David", "Alice"]))


# Function to display data
def display_data():
    print("\nList of Users:")
    print(user_manager.list_users())

    print("\nList of Expenses:")
    for expense in expense_manager.list_expenses():
        print(expense)



# Function to settle debts
def settle_debts():
    print("\nSettling debts...")
    transactions = expense_manager.settle_debt()
    for transaction in transactions:
        print(transaction)


# Main logic
if __name__ == "__main__":
    # Add sample data
    #add_sample_data()

    # Display current data
    display_data()

    # Settle debts and display the results
    #settle_debts()

    # Close the database connection
    #db.close()
