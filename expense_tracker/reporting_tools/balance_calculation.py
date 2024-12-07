class BalanceManager:
    def __init__(self, db):
        self.db = db
    
    def calculate_balances(self):
        # Fetch all expenses, unused now
        self.db.cursor.execute("SELECT payer, amount, participants FROM expenses")
        expenses = self.db.cursor.fetchall()

        # Calculate balances
        for payer, amount, participants in expenses:
            participants_list = participants.split(",")
            share = amount / len(participants_list)

            # Update payer's balance
            self.db.cursor.execute("""
                INSERT INTO balances (user, balance) 
                VALUES (?, ?) ON CONFLICT(user) DO UPDATE SET balance = balance + ?
            """, (payer, amount - share * len(participants_list),amount + share * len(participants_list)))

            # Update participants' balances
            for participant in participants_list:
                if participant != payer:
                    #print("executed:" ,participant, -share,share)
                    self.db.cursor.execute("""
                        INSERT INTO balances (user, balance) 
                        VALUES (?, ?) ON CONFLICT(user) DO UPDATE SET balance = balance - ?
                        
                    """, (participant, -share,share))

                    '''ON CONFLICT(user) DO UPDATE SET balance = balance - ?'''
        # Commit the changes
        self.db.conn.commit()

    def calculate_debts(self):
        #fixed bugs in SQL, now ensure unique (creditor, debtor) pairs in either (debtor, creditor) or (creditor, debtor)
        #pending: need to handle problem of owing negative amount
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
                            self.db.conn.commit()
                        else:
                            # Reverse the amount since the roles are reversed
                            self.db.cursor.execute(
                                "UPDATE debts SET amount = amount - ? WHERE creditor = ? AND debtor = ?",
                                (share, participant, payer)
                            )
                            self.db.conn.commit()
                    else:
                        # No existing debt
                        self.db.cursor.execute(
                            "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
                            (payer, participant, share)
                        )
                        self.db.conn.commit()
                    '''
                    self.db.cursor.execute(
                        """
                        INSERT INTO debts (creditor, debtor, amount)
                        VALUES (?, ?, ?)
                        ON CONFLICT(creditor, debtor) DO UPDATE SET amount = amount + ?
                        ON CONFLICT(debtor,creditor) DO UPDATE SET amount = amount + ?""",
                        (payer, participant, share, share, -share)
                    )
                    '''

                    '''ON CONFLICT(creditor, debtor) DO UPDATE SET amount = amount + ?'''
        #self.db.conn.commit()

    def simplify_debts(self):
        """Simplify debt relationships to minimize transactions."""
        debts = self.db.cursor.execute("SELECT * FROM debts").fetchall()
        debt_map = {}  # {creditor: {debtor: amount}}

        # Build a debt map
        for debt in debts:
            creditor, debtor, amount = debt[1], debt[2], debt[3]
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





