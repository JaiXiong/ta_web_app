import unittest as ut
from ta_app.account_object import Account


class TestAccountObject(ut.TestCase):

    # tests setting user property
    def test_account1(self):
        ac = Account("test1User", "test1Password", "Supervisor")
        self.assertEqual(ac.user, "test1User")

    # tests setting password property
    def test_account2(self):
        ac = Account("test2User", "test2Password", "Supervisor")
        self.assertEqual(ac.password, "test2Password")

    # tests setting role property
    def test_account3(self):
        ac = Account("test3User", "test3Password", "Supervisor")
        self.assertEqual(ac.role, "Supervisor")

    # tests a blank username
    def test_account4(self):
        ac = Account("test4User", "test4Password", "Supervisor")
        with self.assertRaises(ValueError):
            ac.user = ""

    # tests a blank password
    def test_account5(self):
        ac = Account("test5User", "test5Password", "Supervisor")
        with self.assertRaises(ValueError):
            ac.password = ""

    # tests a blank role -
    def test_account6(self):
        ac = Account("test6User", "test6Password", "Supervisor")
        with self.assertRaises(ValueError):
            ac.role = ""

    # tests an incorrect role
    def test_account7(self):
        ac = Account("test7User", "test7Password", "Supervisor")
        with self.assertRaises(ValueError):
            ac.role = "cabbage"

    # test the __str__ method
    def test_account8(self):
        ac = Account("user", "password", "Supervisor")
        ac.street_address = "street address"
        ac.email_address = "email address"
        ac.phone_number = "phone number"
        test7str = ac.__str__()
        self.assertEqual(test7str, "user, password, Supervisor, street address, email address, phone number")
