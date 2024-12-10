import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class ReportGeneration:
    def __init__(self, db):
        self.db = db

    def generate_summary(self, user):
        """
        Generate a well-formatted text summary of the user's expense history and debt situation.

        Parameters:
            user (str): The username for which the summary is generated.

        Returns:
            str: The formatted summary as a string.
        """
        # Fetch all expenses involving the user
        self.db.cursor.execute(
            "SELECT * FROM expenses WHERE payer = ? OR participants LIKE ?", (user, f"%{user}%")
        )
        expenses = self.db.cursor.fetchall()

        # Fetch all debts involving the user
        self.db.cursor.execute(
            """
            SELECT debtor, creditor, amount
            FROM debts
            WHERE debtor = ? OR creditor = ?
            """,
            (user, user),
        )
        debts = self.db.cursor.fetchall()

        # Generate the well-formatted summary
        summary = f"### Expense Report for {user} (Generated on {datetime.now()}):\n"

        # Add user's expense history
        summary += "\n**Expense History:**\n"
        if expenses:
            for expense in expenses:
                payer = expense[1]
                amount = expense[2]
                participants = expense[3]
                summary += f"- Payer: {payer}, Amount: ${amount:.2f}, Participants: {participants}\n"
        else:
            summary += "- No expense history found.\n"

        # Add user's debt situation
        summary += "\n**Debt Situation:**\n"
        total_credit = 0
        total_debt = 0
        if debts:
            for debtor, creditor, amount in debts:
                if debtor == user:
                    summary += f"- You owe {creditor}: ${amount:.2f}\n"
                    total_debt += amount
                elif creditor == user:
                    summary += f"- {debtor} owes you: ${amount:.2f}\n"
                    total_credit += amount
        else:
            summary += "- No debt records found.\n"

        # Add totals
        summary += f"\n**Summary:**\n"
        summary += f"- Total Amount You Owe: ${total_debt:.2f}\n"
        summary += f"- Total Amount Owed to You: ${total_credit:.2f}\n"

        return summary


    def export_report(self, user, file_format="txt"):
        """
        Export the summary report for a specific user to a file.

        Parameters:
            user (str): The username for which the report is generated.
            file_format (str): File format to export ("txt", "csv", or "xlsx").
        """
        # Generate the summary
        summary_text = self.generate_summary(user)

        # Define the file name based on the user and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{user}_expense_report_{timestamp}"

        if file_format == "txt":
            # Export as a text file
            with open(f"{file_name}.txt", "w") as file:
                file.write(summary_text)
        elif file_format == "csv":
            # Extract debts from the database
            debts = [
                {"Debtor": debt[0], "Creditor": debt[1], "Amount": debt[2]}
                for debt in self.db.cursor.execute(
                    "SELECT debtor, creditor, amount FROM debts WHERE debtor = ? OR creditor = ?",
                    (user, user),
                ).fetchall()
            ]
            
            # Write debts to a CSV file
            with open(f"{file_name}.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Debtor", "Creditor", "Amount"])
                writer.writeheader()
                writer.writerows(debts)
        elif file_format == "xlsx":
            # Extract debts for Excel export
            debts = [
                {"Debtor": debt[0], "Creditor": debt[1], "Amount": debt[2]}
                for debt in self.db.cursor.execute(
                    "SELECT debtor, creditor, amount FROM debts WHERE debtor = ? OR creditor = ?",
                    (user, user),
                ).fetchall()
            ]

            # Write debts to an Excel file
            df = pd.DataFrame(debts)
            df.to_excel(f"{file_name}.xlsx", index=False)
        else:
            raise ValueError("Invalid file format. Choose 'txt', 'csv', or 'xlsx'.")



    def visualize_balances(self, user):
        """
        Create a pie chart summarizing:
        - Total amount the user owes (negative balances).
        - Total amount owed to the user (positive balances).

        Parameters:
            user (str): The username for whom to generate the visualization.
        """
        # Fetch data for debts owed to the user (creditors) and debts the user owes (debtors)
        creditors = self.db.cursor.execute(
            "SELECT debtor, amount FROM debts WHERE creditor = ?", (user,)
        ).fetchall()

        debtors = self.db.cursor.execute(
            "SELECT creditor, amount FROM debts WHERE debtor = ?", (user,)
        ).fetchall()

        # Calculate totals
        total_owed_to_user = sum(row[1] for row in creditors)
        total_user_owes = sum(row[1] for row in debtors)

        # Handle the case where both totals are 0
        if total_owed_to_user == 0 and total_user_owes == 0:
            print(f"No debts found for {user}.")
            return

        # Prepare data for the chart
        labels = ["Owed to You", "You Owe"]
        sizes = [total_owed_to_user, total_user_owes]  # Positive amounts for both
        colors = ["#76c7c0", "#ff6f61"]

        # Create the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            sizes,
            labels=labels,
            autopct=lambda p: f"${p * sum(sizes) / 100:.2f}",
            startangle=90,
            colors=colors,
            wedgeprops={"edgecolor": "black"},
        )
        plt.title(f"Debt Summary for {user}", fontsize=16)
        plt.axis("equal")  # Ensure the pie is a circle
        plt.tight_layout()

        # Show the chart
        plt.show()

