
class ExpenseManager:
    def __init__(self, db):
        self.db = db

    def add_expense(self, payer, amount, participants):
        participants_str = ",".join(participants)

        # Insert expense
        self.db.cursor.execute("""
            INSERT INTO expenses (payer, amount, participants)
            VALUES (?, ?, ?)
        """, (payer, amount, participants_str))

        # Update balances
        split_amount = amount / len(participants)
        for participant in participants:
            if participant != payer:
                # Deduct from participant
                self.db.cursor.execute("""
                    UPDATE balances SET balance = balance - ? WHERE user = ?
                """, (split_amount, participant))
            # Add to payer
            self.db.cursor.execute("""
                UPDATE balances SET balance = balance + ? WHERE user = ?
            """, (amount - split_amount, payer))

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

        payer, amount, participants_str = expense
        participants = participants_str.split(",")
        split_amount = amount / len(participants)

        # Reverse balances
        for participant in participants:
            if participant != payer:
                # Add back to participant
                self.db.cursor.execute("""
                    UPDATE balances SET balance = balance + ? WHERE user = ?
                """, (split_amount, participant))
            # Deduct from payer
            self.db.cursor.execute("""
                UPDATE balances SET balance = balance - ? WHERE user = ?
            """, (amount - split_amount, payer))

        # Remove expense
        self.db.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.db.conn.commit()
        return f"Expense with ID {expense_id} removed successfully."

    import sqlite3

    def settle_debt(payer: str, receiver: str, amount: float):
        """
        Settle a portion of the debt by recording a payment from the payer to the receiver.

        Args:
            payer (str): The name of the person making the payment.
            receiver (str): The name of the person receiving the payment.
            amount (float): The amount being paid.

        Raises:
            ValueError: If the amount is not positive or if no debt exists between the payer and receiver.
        """
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        # Connect to the SQLite database
        conn = sqlite3.connect("debts.db")
        cursor = conn.cursor()

        try:
            # Check if a debt exists between the payer and receiver
            cursor.execute("""
                SELECT amount
                FROM debts
                WHERE payer = ? AND receiver = ?
            """, (payer, receiver))
            debt = cursor.fetchone()

            if not debt:
                raise ValueError(f"No debt found between {payer} and {receiver}.")

            current_debt = debt[0]

            if amount > current_debt:
                raise ValueError(f"Payment exceeds the outstanding debt of {current_debt:.2f}.")

            # Update the debt amount
            new_debt = current_debt - amount
            if new_debt == 0:
                # Delete the debt record if fully paid
                cursor.execute("""
                    DELETE FROM debts
                    WHERE payer = ? AND receiver = ?
                """, (payer, receiver))
            else:
                # Update the debt record with the reduced amount
                cursor.execute("""
                    UPDATE debts
                    SET amount = ?
                    WHERE payer = ? AND receiver = ?
                """, (new_debt, payer, receiver))

            # Commit changes
            conn.commit()
            print(f"Payment of {amount:.2f} from {payer} to {receiver} recorded successfully.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


