# Who Owes Who - Documentation

## Overview
`Who Owes Who` is a Python package designed to manage shared expenses among users. It provides functionality to track expenses, calculate balances, simplify debts, and generate reports.

---

## Modules and Key Functions

### **1. Database Management (`db_management.py`)**
Handles database initialization and table creation.

- **`DatabaseManager`**
  - Initializes the SQLite database and creates required tables (`users`, `expenses`, `balances`, `debts`).

---

### **2. User Management (`user_management.py`)**
Manages user-related operations.

- **`add_user(name: str, balance: float)`**
  - Adds a user to the database with an optional initial balance.

- **`remove_user(name: str)`**
  - Removes a user and their associated balances.

- **`list_users()`**
  - Lists all registered users.

---

### **3. Expense Management (`expense_operations.py`)**
Tracks and manages expenses.

- **`add_expense(payer: str, amount: float, participants: list)`**
  - Records a new expense, splitting the amount among participants.

- **`list_expenses()`**
  - Lists all recorded expenses.

- **`settle_debt(payer: str, receiver: str, amount: float)`**
  - Settles a portion of a debt between two users.

---

### **4. Balance Calculation (`balance_calculation.py`)**
Calculates user balances and simplifies debts.

- **`calculate_balances()`**
  - Calculates net balances for all users.

- **`calculate_debts()`**
  - Computes detailed debts between creditors and debtors.

- **`simplify_debts()`**
  - Suggests simplified debt relationships.

- **`get_user_debts(user: str)`**
  - Retrieves debts specific to a user.

---

### **5. Reporting Tools (`report_generation.py`)**
Generates summaries and visualizations.

- **`generate_summary(format: str)`**
  - Summarizes expenses and debts in text or JSON format.

- **`export_report(file_format: str)`**
  - Exports the report in TXT, CSV, or XLSX format.

- **`visualize_debts(save_to_file: bool)`**
  - Visualizes debts using bar and pie charts.

---

### Usage Flow
1. Add users using `add_user`.
2. Record expenses using `add_expense`.
3. View balances and debts using `calculate_balances` and `calculate_debts`.
4. Generate reports and visualizations using `report_generation`.

---

## Example Usage
Refer to the test file (`test_package.py`) for detailed usage.
