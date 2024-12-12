import unittest
from expense_operations import ExpenseManager
import sqlite3

class TestExpenseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cls.conn.execute("CREATE TABLE expenses (id INTEGER PRIMARY KEY, payer TEXT, amount REAL CHECK(TYPEOF(amount) = 'real'), participants TEXT)")
        cls.conn.execute("CREATE TABLE debts (creditor TEXT, debtor TEXT, amount REAL)")
        cls.cursor = cls.conn.cursor()
        cls.manager = ExpenseManager(db=cls)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("DELETE FROM expenses")
        self.cursor.execute("DELETE FROM debts")
        self.conn.commit()

    def tearDown(self):
        pass

    def test_add_expense(self):
        result = self.manager.add_expense("Alice", 100, ["Alice", "Bob"])
        self.assertIn("Alice", result)
        self.assertIn("100", result)
        self.assertEqual(len(self.manager.list_expenses()), 1)
        self.assertEqual(self.manager.list_expenses()[0][1], "Alice")

        with self.assertRaises(TypeError):
            self.manager.add_expense("Alice",10,[1,2])

        with self.assertRaises(sqlite3.IntegrityError):
            self.manager.add_expense("Alice","asd",["Alice", "Bob"])

        with self.assertRaises(Exception):
            self.manager.add_expense(None,None,None)


    def test_remove_expense(self):
        self.manager.add_expense("Alice", 100, ["Alice", "Bob"])
        self.assertEqual(len(self.manager.list_expenses()), 1)
        self.manager.add_expense("Bob", 100, ["Alice", "Bob","Peter"])
        self.assertEqual(len(self.manager.list_expenses()), 2)
        result = self.manager.remove_expense(1)

        self.assertIn("removed", result)
        self.assertIn("ID 1", result)
        self.assertEqual(len(self.manager.list_expenses()), 1)

        #remove non exist expense
        #res = self.manager.remove_expense(-1)
        #self.assertEqual(res,"Expense with ID -1 does not exist.")

        # Remove a non-existent expense
        #result = self.manager.remove_expense(99)
        #self.assertEqual(result, "Expense with ID 99 does not exist.")

        with self.assertRaises(sqlite3.IntegrityError):
            self.manager.remove_expense(-1)

    def test_list_expenses(self):
        self.manager.add_expense("Alice", 100, ["Alice", "Bob"])
        self.manager.add_expense("Bob", 50, ["Alice", "Bob", "Charlie"])
        expenses = self.manager.list_expenses()
        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0][1], "Alice")
        self.assertEqual(expenses[1][1], "Bob")
        #print(expenses)

        #test whether member in participants
        self.assertIn("Alice", expenses[0][3])
        self.assertIn("Charlie", expenses[1][3])

        # Test no expenses
        self.setUp()
        self.assertEqual(len(self.manager.list_expenses()), 0)

    def test_settle_debt(self):
        self.cursor.execute("INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)", ("Alice", "Bob", 50))
        self.cursor.execute("INSERT INTO debts (creditor, debtor, amount) VALUES (?, ?, ?)", ("Alice", "Charlie", 30))
        self.conn.commit()

        # Test settling debt
        result = self.manager.settle_debt("Bob", "Alice", 20)
        self.assertIsNone(result)  #return none

        self.cursor.execute("SELECT amount FROM debts WHERE creditor = 'Alice' AND debtor = 'Bob'")
        bob_debt = self.cursor.fetchone()[0]
        self.assertEqual(bob_debt, 30)

        self.cursor.execute("SELECT amount FROM debts WHERE creditor = 'Alice' AND debtor = 'Charlie'")
        charlie_debt = self.cursor.fetchone()[0]
        self.assertEqual(charlie_debt, 30)

        #negative amount
        with self.assertRaises(ValueError):
            self.manager.settle_debt("Bob", "Alice", -10)

        #no such record in debts
        with self.assertRaises(ValueError):
            self.manager.settle_debt("David", "Alice", 50)

        with self.assertRaises(TypeError):
            self.manager.settle_debt("Bob", "Alice", "asd")

        # Settle full debt
        result = self.manager.settle_debt("Bob", "Alice", 30)
        self.assertIsNone(result)
        self.cursor.execute("SELECT amount FROM debts WHERE creditor = 'Alice' AND debtor = 'Bob'")
        bob_debt = self.cursor.fetchone()
        self.assertEqual(bob_debt[0],0)  # Debt should no longer exist


if __name__=='__main__':
    unittest.main()
