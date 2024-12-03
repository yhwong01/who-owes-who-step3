from expense_tracker.expense_management.db_management import *

class BalanceManager:
    def __init__(self, db):
        self.db = db
    
    def calculate_balances(self):
        """Calculate detailed debts between users."""
        self.db.cursor.execute("DELETE FROM debts")
        self.db.cursor.execute("SELECT * FROM expenses")

        for expense in self.db.cursor.fetchall():
            payer = expense["payer"]
            amount = expense["amount"]
            participants = expense["participants"].split(",")
            share = amount / len(participants)

        for participant in participants:
            if participant != payer:
                self.db.cursor.execute(
                    """
                    INSERT INTO debts (creditor, debtor, amount)
                    VALUES (?, ?, ?)
                    ON CONFLICT(creditor, debtor)
                    DO UPDATE SET amount = amount + ?
                    """,
                    (payer, participant, share, share)
                )
                    
        self.db.conn.commit()

    def simplify_debts(self):
        """Simplify debt relationships to minimize transactions."""
        debts = self.db.cursor.execute("SELECT * FROM debts").fetchall()
        debt_map = {}  # {creditor: {debtor: amount}}

        # Build a debt map
        for debt in debts:
            creditor, debtor, amount = debt["creditor"], debt["debtor"], debt["amount"]
            debt_map.setdefault(creditor, {}).setdefault(debtor, 0)
            debt_map[creditor][debtor] += amount

        # Update the debts table with simplified values
        self.db.cursor.execute("DELETE FROM debts")  # Clear old debts
        for creditor, relations in debt_map.items():
            for debtor, amount in relations.items():
                if amount > 0:
                    self.db.cursor.execute(
                        "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
                        (creditor, debtor, amount)
                    )
        self.db.conn.commit()

    def get_user_debts(self, user):
        """Retrieve detailed debt information for a specific user."""
        creditors = self.db.cursor.execute(
            "SELECT debtor, amount FROM debts WHERE creditor = ?", (user,)
        ).fetchall()

        debtors = self.db.cursor.execute(
            "SELECT creditor, amount FROM debts WHERE debtor = ?", (user,)
        ).fetchall()

        result = {
            "owed_by_others": [{"debtor": row["debtor"], "amount": row["amount"]} for row in creditors],
            "owes_to_others": [{"creditor": row["creditor"], "amount": row["amount"]} for row in debtors],
        }
        return result



