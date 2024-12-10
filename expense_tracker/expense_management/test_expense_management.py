from expense_tracker.expense_management.db_management import DatabaseManager
from user_management import UserManager
from expense_operations import ExpenseManager

# Initialize the database and managers
db = DatabaseManager(db_name="../expense_tracker.db")
user_manager = UserManager(db)
expense_manager = ExpenseManager(db)

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

if __name__ == "__main__":
    # Add sample data
    #add_sample_data()
    user_manager.remove_user("Charlie")

    print(expense_manager.remove_expense(7))
    display_data()
    exit(2)
    user_manager.add_user("Jacob")
    user_manager.add_user("Peter",10000)

    # Query to get balances

    db.cursor.execute("SELECT * from balances;")
    # Fetch all table names
    tables = db.cursor.fetchall()

    # Print the list of tables
    print("Tables in the database:")
    for table in tables:
        print(table)

    # Display current data
    display_data()

    # Settle debts and display the results
    #expense_manager.settle_debt(payer="Alice",receiver="David", amount= 20)
    display_data()

    db.cursor.execute("SELECT * from balances;")
    tables = db.cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table)

    # test balance_calculation
    balance_calculator.calculate_balances()

    # Close the database connection
    db.close()
