import matplotlib.pyplot as plt
from expense_tracker.expense_management.db_management import *

class report_generation:
    def __init__(self, db):
        self.db = db

    def generate_summary(self, format="text"):
        """
        Generate a summary of expenses and debts in text or JSON format.

        Parameters:
            format (str): The desired format ("text" or "json").

        Returns:
            str or dict: The formatted summary.
        """
        self.db.cursor.execute("SELECT * FROM expenses")
        expenses = self.db.cursor.fetchall()

        self.db.cursor.execute("SELECT debtor, creditor, amount FROM debts")
        debts = self.db.cursor.fetchall()
        self.db.close()

        if format == "text":
            summary = "Expense Summary:\n"
            for expense in expenses:
                summary += f"- Payer: {expense[1]}, Amount: {expense[2]}, Participants: {expense[3]}\n"
            summary += "\nDebt Summary:\n"
            for debt in debts:
                summary += f"- Debtor: {debt[0]}, Creditor: {debt[1]}, Amount: {debt[2]}\n"
            return summary
        elif format == "json":
            summary = {
                "expenses": [{"payer": e[1], "amount": e[2], "participants": e[3]} for e in expenses],
                "debts": [{"debtor": d[0], "creditor": d[1], "amount": d[2]} for d in debts],
            }
            return summary
        else:
            raise ValueError("Invalid format. Choose 'text' or 'json'.")

    def export_report(self, format="txt"):
        """
        Export the summary report to a file.

        Parameters:
            format (str): File format ("txt" or "csv").
        """
        summary = self.generate_summary(format="text" if format == "txt" else "json")

        if format == "txt":
            with open("report.txt", "w") as file:
                file.write(summary)
        elif format == "csv":
            import csv
            with open("report.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Debtor", "Creditor", "Amount"])
                for debt in summary["debts"]:
                    writer.writerow([debt["debtor"], debt["creditor"], debt["amount"]])
        else:
            raise ValueError("Invalid format. Choose 'txt' or 'csv'.")
        

    def visualize_debts(self):
        """
        Visualize debts using bar and pie charts.
        """
        self.db.cursor.execute("SELECT debtor, creditor, amount FROM debts")
        debts = self.db.cursor.fetchall()
        self.db.close()

        # Aggregate debts by debtor for visualization
        debtor_totals = {}
        for debt in debts:
            debtor_totals[debt[0]] = debtor_totals.get(debt[0], 0) + debt[2]

        # Bar chart
        debtors = list(debtor_totals.keys())
        amounts = list(debtor_totals.values())
        plt.bar(debtors, amounts, color="salmon")
        plt.title("Debts per Debtor")
        plt.xlabel("Debtor")
        plt.ylabel("Total Amount Owed")
        plt.show()

        # Pie chart (optional)
        plt.pie(amounts, labels=debtors, autopct="%1.1f%%", startangle=90)
        plt.title("Debt Distribution")
        plt.axis("equal")
        plt.show()

