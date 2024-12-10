class BalanceManager:
    def __init__(self, db):
        self.db = db

    def calculate_debts(self):
        #fixed bugs in SQL, now ensure unique (creditor, debtor) pairs in either (debtor, creditor) or (creditor, debtor)
        """Calculate detailed debts between users."""
        self.db.cursor.execute("DELETE FROM debts")
        self.db.cursor.execute("SELECT * FROM expenses")

        for expense in self.db.cursor.fetchall():
            payer = expense[1] # access payer
            amount = expense[2] # access amount
            participants = expense[3].split(",")
            share = amount / len(participants)
            print(payer,amount,participants)

            for participant in participants:
                if participant != payer:
                    # Check if an existing debt exist
                    existing_debt = self.db.cursor.execute(
                        "SELECT creditor, debtor, amount FROM debts WHERE (creditor = ? AND debtor = ?) OR (creditor = ? AND debtor = ?)",
                        (payer, participant, participant, payer)
                    ).fetchone()

                    if existing_debt:
                        creditor, debtor, amount = existing_debt
                        if creditor == payer:
                            # Update the existing record
                            self.db.cursor.execute(
                                "UPDATE debts SET amount = amount + ? WHERE creditor = ? AND debtor = ?",
                                (share, payer, participant)
                            )
                        else:
                            # Reverse the amount since the roles are reversed
                            self.db.cursor.execute(
                                "UPDATE debts SET amount = amount - ? WHERE creditor = ? AND debtor = ?",
                                (share, participant, payer)
                            )
                    else:
                        # No existing debt, insert a new debt relationship
                        self.db.cursor.execute(
                            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
                            (payer, participant, share)
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
            creditor, debtor, amount = debt[1], debt[2], debt[3]
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
        if creditors:
            print("### Amounts Owed to You (Creditors):")
            for debtor, amount in creditors:
                print(f"- {debtor} owes you: ${amount:.2f}")
        else:
            print("### Amounts Owed to You (Creditors): None")

        if debtors:
            print("\n### Amounts You Owe (Debtors):")
            for creditor, amount in debtors:
                print(f"- You owe {creditor}: ${amount:.2f}")
        else:
            print("\n### Amounts You Owe (Debtors): None")

        return

    def update_negative_debts(self):
        """Interchange the creditor and debtor if the debt amount is negative."""
        neg_debt = self.db.cursor.execute(
            "SELECT creditor,debtor,amount FROM debts WHERE amount < 0"
        ).fetchall()

        if neg_debt:
            print("### Amounts Owed to You (Creditors):",)
            for creditor,debtor,amount in neg_debt:
                print(creditor,debtor,amount)
                self.db.cursor.execute("INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)", (debtor, creditor, amount*-1))
                self.db.conn.commit()
                self.db.cursor.execute("delete from debts where creditor = ? and debtor = ?", (creditor,debtor,))
                self.db.conn.commit()

            print("\n### Converted negative debts successfully")
        else:
            print("### No negative debts found")
        return





