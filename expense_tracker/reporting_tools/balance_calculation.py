class BalanceManager:
    def __init__(self, db):
        self.db = db
    
    def calculate_balances(self):
        # Fetch all expenses
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
                    self.db.cursor.execute(
                        """
                        INSERT INTO debts (creditor, debtor, amount)
                        VALUES (?, ?, ?)
                        ON CONFLICT(creditor, debtor) DO UPDATE SET amount = amount + ?""",
                        (payer, participant, share, share)
                    )

                    '''ON CONFLICT(creditor, debtor) DO UPDATE SET amount = amount + ?'''
        self.db.conn.commit()

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
        print("creditors")
        for item in creditors:
            print(item)

        print("debtors")
        for item in debtors:
            print(item)
        '''result = {
            "owed_by_others": [{"debtor": row["debtor"], "amount": row["amount"]} for row in creditors],
            "owes_to_others": [{"creditor": row["creditor"], "amount": row["amount"]} for row in debtors],
        }'''
        #return result
        return



