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


    # def simplify_debts(self):
    #     """
    #     Suggest debt simplifications where transfers can happen between users who already have a debt relationship.

    #     Returns:
    #         list: Human-readable suggestions for debt transfers and instructions for unresolved relationships.
    #     """
    #     # Fetch all debts from the database
    #     debts = self.db.cursor.execute(
    #         "SELECT creditor, debtor, amount FROM debts"
    #     ).fetchall()

    #     # Build a debt map to track relationships
    #     debt_map = {}  # {debtor: {creditor: amount}}
    #     for creditor, debtor, amount in debts:
    #         debt_map.setdefault(debtor, {})[creditor] = amount

    #     # Prepare suggestions for simplification
    #     suggestions = []

    #     # Iterate through each debtor and their creditors
    #     for debtor, creditors in debt_map.items():
    #         for creditor, amount in creditors.items():
    #             # Check if the creditor also owes someone
    #             if creditor in debt_map:
    #                 for next_creditor, next_amount in debt_map[creditor].items():
    #                     # Suggest a transfer if there's a known relationship
    #                     if next_creditor == debtor or next_creditor in creditors:
    #                         suggested_amount = min(amount, next_amount)
    #                         suggestions.append((creditor, next_creditor, suggested_amount))

    #     # Create human-readable output
    #     readable_suggestions = []
    #     for debtor, creditor, amount in suggestions:
    #         readable_suggestions.append(
    #             f"{debtor} should directly transfer ${amount:.2f} to {creditor} to simplify debts."
    #         )

    #     # Provide instructions for unresolved relationships
    #     unresolved = []
    #     for creditor, debtor, amount in debts:
    #         if (creditor, debtor, amount) not in suggestions:
    #             unresolved.append(
    #                 f"No simplification possible for {debtor} owing ${amount:.2f} to {creditor}. Please settle this directly."
    #             )

    #     return {"simplifications": readable_suggestions, "instructions": unresolved}



    def get_user_debts(self, user):
        """Retrieve detailed debt information for a specific user."""
        creditors = self.db.cursor.execute(
            "SELECT debtor, amount FROM debts WHERE creditor = ?", (user,)
        ).fetchall()

        debtors = self.db.cursor.execute(
            "SELECT creditor, amount FROM debts WHERE debtor = ?", (user,)
        ).fetchall()

        if creditors:
            total_credit = sum(amount for _, amount in creditors)
            print("### Amounts Owed to You:")
            for debtor, amount in creditors:
                print(f"- {debtor} owes you: ${amount:.2f}")
            print(f"\n💰Total Amount Owed to You: ${total_credit:.2f}")
        else:
            print("### Amounts Owed to You: No one owes you money.")

        if debtors:
            total_debt = sum(amount for _, amount in debtors)
            print("\n### Amounts You Owe:")
            for creditor, amount in debtors:
                print(f"- You owe {creditor}: ${amount:.2f}")
            print(f"\n💰Total Amount You Owe: ${total_debt:.2f}")
        else:
            print("\n### Amounts You Owe: You don’t owe anyone money.\n")

        return

    # def update_negative_debts(self):
    #     """Interchange the creditor and debtor if the debt amount is negative."""
    #     neg_debt = self.db.cursor.execute(
    #         "SELECT creditor,debtor,amount FROM debts WHERE amount < 0"
    #     ).fetchall()

    #     if neg_debt:
    #         print("### Amounts Owed to You (Creditors):",)
    #         for creditor,debtor,amount in neg_debt:
    #             print(creditor,debtor,amount)
    #             self.db.cursor.execute("INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)", (debtor, creditor, amount*-1))
    #             self.db.conn.commit()
    #             self.db.cursor.execute("delete from debts where creditor = ? and debtor = ?", (creditor,debtor,))
    #             self.db.conn.commit()

    #         print("\n### Converted negative debts successfully")
    #     else:
    #         print("### No negative debts found")
    #     return

    def update_negative_debts(self):
        """Interchange the creditor and debtor if the debt amount is negative."""
        neg_debt = self.db.cursor.execute(
            "SELECT creditor, debtor, amount FROM debts WHERE amount < 0"
        ).fetchall()

        for row in neg_debt:
            if len(row) != 3:
                raise ValueError(f"Unexpected row format: {row}")
            creditor, debtor, amount = row

            # Convert negative debt
            self.db.cursor.execute(
                "INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)",
                (debtor, creditor, -amount)
            )
            self.db.conn.commit()

            # Delete the original negative debt
            self.db.cursor.execute(
                "DELETE FROM debts WHERE creditor = ? AND debtor = ?",
                (creditor, debtor)
            )
            self.db.conn.commit()

        print("\n### Converted negative debts successfully")
