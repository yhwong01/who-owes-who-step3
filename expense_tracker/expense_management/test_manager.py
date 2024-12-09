import unittest
from expense_operations import Manager

class TestManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = Manager(name="TestManager")


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_manager_name(self):
        self.assertEqual(self.manager.name, "TestManager")
        self.assertIsInstance(self.manager, Manager)
        self.assertNotEqual(self.manager.name, "ExpenseManager")
        self.assertTrue(hasattr(self.manager, "__str__"))

    def test_str_method(self):
        self.assertEqual(str(self.manager), "TestManager")
        self.assertIsInstance(str(self.manager), str)
        self.assertIn("Test", str(self.manager))
        self.assertNotIn("Fail", str(self.manager))

if __name__=='__main__':
    unittest.main()