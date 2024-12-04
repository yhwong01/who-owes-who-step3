#from expense_tracker.expense_management.test import expense_manager


class BalanceManager:
    def __init__(self, db):
        self.db = db
    
    def calculate_balances(self):
        # Fetch all expenses
        self.db.cursor.execute("SELECT payer, amount, participants FROM expenses")
        expenses = self.db.cursor.fetchall()

        #added
        print(expenses)
        # Reset balances
        self.db.cursor.execute("UPDATE balances SET balance = 0")

        # Calculate balances
        for payer, amount, participants in expenses:
            participants_list = participants.split(",")
            share = amount / len(participants_list)

            # Update payer's balance
            self.db.cursor.execute("""
                INSERT INTO balances (user, balance) 
                VALUES (?, ?) 
                ON CONFLICT(user) DO UPDATE SET balance = balance + ?
            """, (payer, amount - share * len(participants_list), amount - share * len(participants_list)))

            # Update participants' balances
            for participant in participants_list:
                if participant != payer:
                    self.db.cursor.execute("""
                        INSERT INTO balances (user, balance) 
                        VALUES (?, ?) 
                        ON CONFLICT(user) DO UPDATE SET balance = balance - ?
                    """, (participant, -share, share))

        # Commit the changes
        self.db.conn.commit()

    def calculate_debts(self):
        """Calculate detailed debts between users."""
        self.db.cursor.execute("DELETE FROM debts")
        self.db.cursor.execute("SELECT * FROM expenses")

        for expense in self.db.cursor.fetchall():
            payer = expense[1] # access payer
            amount = expense[2] # access amount
            participants = expense[3].split(",")
            share = amount / len(participants)

            payer = expense[1]
            amount = expense[2]
            participants = expense[3].split(",")
            share = amount / len(participants)
            print(payer,amount,participants)

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
        """
        Simplify debt relationships to minimize transactions.
        """
        debts = self.db.cursor.execute("SELECT creditor, debtor, amount FROM debts").fetchall()
        debt_map = {}  # {creditor: {debtor: amount}}

        # Build a debt map from the existing debts
        for debt in debts:
            creditor, debtor, amount = debt
            debt_map.setdefault(creditor, {}).setdefault(debtor, 0)
            debt_map[creditor][debtor] += amount

        # Create a net balance map from the debt map
        net_balances = {}  # {person: net_balance}
        for creditor, relations in debt_map.items():
            for debtor, amount in relations.items():
                net_balances[creditor] = net_balances.get(creditor, 0) + amount
                net_balances[debtor] = net_balances.get(debtor, 0) - amount

        # Separate people into creditors and debtors
        creditors = [(person, balance) for person, balance in net_balances.items() if balance > 0]
        debtors = [(person, -balance) for person, balance in net_balances.items() if balance < 0]

        # Simplify transactions
        simplified_transactions = []
        while creditors and debtors:
            creditor, credit_amount = creditors.pop(0)
            debtor, debt_amount = debtors.pop(0)

            settled_amount = min(credit_amount, debt_amount)
            simplified_transactions.append((debtor, creditor, settled_amount))

            credit_remaining = credit_amount - settled_amount
            debt_remaining = debt_amount - settled_amount

            if credit_remaining > 0:
                creditors.insert(0, (creditor, credit_remaining))
            if debt_remaining > 0:
                debtors.insert(0, (debtor, debt_remaining))

        # Update the debts table with simplified values
        self.db.cursor.execute("DELETE FROM debts")  # Clear old debts
        for debtor, creditor, amount in simplified_transactions:
            self.db.cursor.execute(
                "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
                (creditor, debtor, amount)
            )
        self.db.conn.commit()

        return simplified_transactions


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



