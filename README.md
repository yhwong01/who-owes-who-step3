# Who Owes Who - Documentation

![Passing Build Stamp](https://app.travis-ci.com/yhwong01/who-owes-who-step3.svg?token=sSxpVi7UMFCV6y91PqY5&branch=main)

## Overview
`Who Owes Who` is a Python package designed to manage shared expenses among users. It provides functionality to track expenses, calculate balances, simplify debts, and generate reports with detailed visualizations. This package is built for users who need to manage group expenses efficiently and keep track of debts.

---

## Demo and Installation

- **[Demo Video](https://youtu.be/uTXSjDfg8Ms)**
- **[PyPI Package](https://pypi.org/project/who-owes-who/0.1.0/)**

---

## Key Functionalities

### **1. Database Management (`db_management.py`)**
Handles database initialization and table creation.

- **`DatabaseManager`**
  - Initializes the SQLite database and creates required tables (`users`, `expenses`, `balances`, `debts`).

---

### **2. User Management (`user_management.py`)**
Manages user-related operations.

- **`add_user(name: str)`**
  - Adds a user to the database.
- **`remove_user(name: str)`**
  - Removes a user and their associated balances and debts.
- **`list_users()`**
  - Lists all registered users.

---

### **3. Expense Management (`expense_operations.py`)**
Tracks and manages expenses.

- **`add_expense(payer: str, amount: float, participants: list)`**
  - Records a new expense, splitting the amount among participants.
- **`remove_expense(id: int)`**
  - Deletes an existing expense by its ID.
- **`list_expenses()`**
  - Lists all recorded expenses.

---

### **4. Balance Calculation (`balance_calculation.py`)**
Calculates user balances and simplifies debts.

- **`calculate_balances()`**
  - Calculates net balances for all users.
- **`calculate_debts()`**
  - Computes detailed debts between creditors and debtors.
- **`get_user_debts(user: str)`**
  - Retrieves debts specific to a user.
- **`update_negative_debts()`**
  - Converts negative debt balances to proper positive entries.

---

### **5. Reporting Tools (`report_generation.py`)**
Generates summaries, exports reports, and visualizes data.

- **`generate_summary(user: str)`**
  - Summarizes expenses and debts in a well-formatted string.
- **`export_report(user: str, file_format: str)`**
  - Exports reports in TXT, CSV, or XLSX formats.
- **`visualize_balances(user: str)`**
  - Creates pie charts summarizing debts and balances.

---

## Usage Flow

1. **Initialize Database**: Set up tables using `DatabaseManager`.
2. **Manage Users**:
   - Add users using `add_user`.
   - List users using `list_users`.
   - Remove users using `remove_user`.
3. **Record Expenses**:
   - Add expenses using `add_expense`.
   - List all expenses using `list_expenses`.
   - Remove expenses using `remove_expense`.
4. **Calculate and Simplify Balances**:
   - Use `calculate_balances` to calculate balances.
   - Use `calculate_debts` to compute detailed debts.
   - Use `get_user_debts` to fetch debts for a specific user.
   - Simplify debts with `update_negative_debts`.
5. **Generate Reports and Visualize Data**:
   - Generate a summary using `generate_summary`.
   - Export reports with `export_report`.
   - Visualize debts with `visualize_balances`.

---

## Example Demo
Here’s a quick demo of the package functionalities, as shown in the accompanying video:

1. **Add a New User**: Demonstrated by adding `John` and `Jane`.
2. **Add a New Expense**: John pays $100 for a team lunch with `John, Jane, and Smith`.
3. **List Users**: Displays the list of all users.
4. **List Expenses**: Shows the recorded expenses, including participants.
5. **Remove User**: Removes `Smith` from the database.
6. **Remove Expense**: Deletes an expense entry.
7. **Calculate Debts**: Computes debts between users.
8. **Generate a Report**: Generates a detailed report for `John`.
9. **Visualize Debts**: Creates a pie chart for `John’s` debt situation.
10. **Export Report**: Saves the report as a CSV file.

---

## Example Code

```python
from expense_tracker.reporting_tools.balance_calculation import BalanceManager
from expense_tracker.reporting_tools.report_generation import ReportGeneration
from expense_tracker.expense_management.db_management import DatabaseManager

# Initialize database and managers
db = DatabaseManager("expense_tracker.db")
balance_manager = BalanceManager(db)
report_gen = ReportGeneration(db)

# Add users and expenses
db.cursor.execute("INSERT INTO users (name) VALUES ('John'), ('Jane'), ('Smith')")
db.conn.commit()
balance_manager.calculate_debts()
report_gen.export_report("John", file_format="csv")
```

---

## Contribution
Feel free to fork the repository and submit pull requests for additional features or bug fixes.