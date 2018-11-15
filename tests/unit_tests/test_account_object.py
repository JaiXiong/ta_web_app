import unittest as ut
from unittest import mock
from ta_app.account_object import Account


class TestAccountObject(ut.TestCase):

    # tests setting user property
    def test_account1(self):
        ac = Account()
        ac.user = "test1User"
        self.assertEqual(ac.user, "test1User")

    # tests setting password property
    def test_account2(self):
        ac = Account()
        ac.password = "test2password"
        self.assertEqual(ac.password, "test2password")

    # tests setting role property
    def test_account3(self):
        ac = Account()
        ac.role = "Supervisor"
        self.assertEqual(ac.role, "Supervisor")

    # tests a blank username
    def test_account4(self):
        ac = Account()
        with self.assertRaises(ValueError):
            ac.user = ""

    # tests a blank password
    def test_account5(self):
        ac = Account()
        with self.assertRaises(ValueError):
            ac.password = ""

    # tests a blank role -
    def test_account6(self):
        ac = Account()
        with self.assertRaises(ValueError):
             ac.role = ""

    # test the __str__ method
    def test_account7(self):
        ac = Account()
        ac.user = "user"
        ac.password = "password"
        ac.role = "Supervisor"
        test7str = ac.__str__()
        self.assertEqual(test7str, "user, password, Supervisor")
