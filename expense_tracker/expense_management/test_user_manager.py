import unittest
from user_management import UserManager
import sqlite3

class TestUserManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #set up db in mem
        cls.conn = sqlite3.connect(":memory:")
        cls.conn.execute("CREATE TABLE users (name TEXT PRIMARY KEY)")
        cls.conn.execute("CREATE TABLE balances (user TEXT PRIMARY KEY, balance REAL)")
        cls.cursor = cls.conn.cursor()
        cls.manager = UserManager(db=cls)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("DELETE FROM users")
        self.cursor.execute("DELETE FROM balances")
        self.conn.commit()

    def tearDown(self):
        pass

    def test_add_user(self):
        result = self.manager.add_user("Alice")
        res = self.manager.add_user("Alice")
        self.assertIn("Alice", result)
        self.assertEqual("User 'Alice' already exists.",res)
        self.assertEqual(len(self.manager.list_users()), 1)
        self.assertEqual(self.manager.list_users()[0], "Alice")
        self.assertNotIn("Bob", self.manager.list_users())

    def test_remove_user(self):
        self.manager.add_user("Alice")
        self.assertEqual(len(self.manager.list_users()), 1)
        self.manager.add_user("Bob")
        self.assertEqual(len(self.manager.list_users()), 2)
        result = self.manager.remove_user("Alice")
        self.assertIn("removed", result)
        self.assertEqual(len(self.manager.list_users()), 1)

    def test_list_users(self):
        self.manager.add_user("Alice")
        self.manager.add_user("Bob")
        self.manager.add_user("Charlie")
        users = self.manager.list_users()
        self.assertEqual(len(users), 3)
        self.assertIn("Alice", users)
        self.assertIn("Bob", users)
        self.assertIn("Charlie", users)

if __name__=='__main__':
    unittest.main()