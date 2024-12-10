import matplotlib.pyplot as plt
import os
from datetime import datetime
from expense_tracker.expense_management.db_management import DatabaseManager

class ReportGeneration:
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
        # Fetch expenses and debts from the database
        self.db.cursor.execute("SELECT * FROM expenses")
        expenses = self.db.cursor.fetchall()

        self.db.cursor.execute("SELECT debtor, creditor, amount FROM debts")
        debts = self.db.cursor.fetchall()

        # Generate the summary
        if format == "text":
            print("hi")
            summary = f"Expense Report (Generated on {datetime.now()}):\n"
            summary += "\nExpense Details:\n"
            for expense in expenses:
                summary += f"- Payer: {expense[1]}, Amount: {expense[2]:.2f}, Participants: {expense[3]}\n"
            summary += "\nDebt Details:\n"
            for debt in debts:
                summary += f"- Debtor: {debt[0]}, Creditor: {debt[1]}, Amount: {debt[2]:.2f}\n"
            return summary
        elif format == "json":
            summary = {
                "timestamp": datetime.now().isoformat(),
                "expenses": [{"payer": e[1], "amount": e[2], "participants": e[3]} for e in expenses],
                "debts": [{"debtor": d[0], "creditor": d[1], "amount": d[2]} for d in debts],
            }
            return summary
        else:
            raise ValueError("Invalid format. Choose 'text' or 'json'.")

    def export_report(self, file_format="txt"):
        """
        Export the summary report to a file.

        Parameters:
            file_format (str): File format ("txt", "csv", or "xlsx").
        """
        summary = self.generate_summary(format="text" if file_format == "txt" else "json")
        file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if file_format == "txt":
            with open(f"{file_name}.txt", "w") as file:
                file.write(summary)
        elif file_format == "csv":
            import csv
            with open(f"{file_name}.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Debtor", "Creditor", "Amount"])
                for debt in summary["debts"]:
                    writer.writerow([debt["debtor"], debt["creditor"], debt["amount"]])
        elif file_format == "xlsx":
            import pandas as pd
            df = pd.DataFrame(summary["debts"])
            df.to_excel(f"{file_name}.xlsx", index=False)
        else:
            raise ValueError("Invalid format. Choose 'txt', 'csv', or 'xlsx'.")

    def visualize_debts(self, save_to_file=False):
        """
        Visualize debts using bar and pie charts.

        Parameters:
            save_to_file (bool): Whether to save the charts as files.
        """
        self.db.cursor.execute("SELECT debtor, creditor, amount FROM debts")
        debts = self.db.cursor.fetchall()

        # Aggregate debts by debtor for visualization
        debtor_totals = {}
        for debt in debts:
            debtor_totals[debt[0]] = debtor_totals.get(debt[0], 0) + debt[2]

        # Bar chart
        debtors = list(debtor_totals.keys())
        amounts = list(debtor_totals.values())

        plt.figure(figsize=(10, 6))  # Increase the figure size
        plt.bar(debtors, amounts, color="skyblue", edgecolor="black")
        plt.title("Debts per Debtor", fontsize=14)
        plt.xlabel("Debtor", fontsize=12)
        plt.ylabel("Total Amount Owed", fontsize=12)
        plt.xticks(rotation=45, ha="right", fontsize=10)
        plt.tight_layout()
        if save_to_file:
            plt.savefig("debts_bar_chart.png")
        plt.show()

        # Pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=debtors, autopct="%1.1f%%", startangle=90, textprops={'fontsize': 10})
        plt.title("Debt Distribution", fontsize=14)
        plt.axis("equal")
        if save_to_file:
            plt.savefig("debts_pie_chart.png")
        plt.show()
