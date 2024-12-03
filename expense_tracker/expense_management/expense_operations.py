
class ExpenseManager:
    def __init__(self, db):
        self.db = db

    def add_expense(self, payer, amount, participants):
        participants_str = ",".join(participants) #each participants sperated by a comma
        # need keep track of the definition of participants
        # either the payer is involved or not for calculating balances

        # Insert expense
        self.db.cursor.execute("""
            INSERT INTO expenses (payer, amount, participants)
            VALUES (?, ?, ?)
        """, (payer, amount, participants_str))

        self.db.conn.commit()
        return f"Expense of {amount} added for {payer}, split among {participants}."

    def list_expenses(self):
        self.db.cursor.execute("SELECT * FROM expenses")
        return self.db.cursor.fetchall()

    def remove_expense(self, expense_id):
        # Fetch participants and payer for the expense
        self.db.cursor.execute("SELECT payer, amount, participants FROM expenses WHERE id = ?", (expense_id,))
        expense = self.db.cursor.fetchone()
        if not expense:
            return f"Expense with ID {expense_id} does not exist."

        self.db.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.db.conn.commit()
        return f"Expense with ID {expense_id} removed successfully."



    def settle_debt(self, payer: str, receiver: str, amount: float):
        """
        Settle a portion of the debt by recording a payment from the payer to the receiver.
        """
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        try:

            #update the table by adding a debt paid by payer to receiver
            self.db.cursor.execute("""
                    UPDATE debt_records
                    SET amount = ?
                    WHERE creditor = ? AND debtor = ?
                """, (amount, receiver, payer))

            # Commit changes
            self.db.conn.commit()
            return print(
                f"Payment of {amount:.2f} from {payer} to {receiver} recorded successfully.")
        except Exception as e:
            self.db.conn.rollback()
            raise e



