#Gus
import unittest as ut
from ui import self


class TestCreateAccount(ut.TestCase):

    def setUp(self):
        self.ui = self()

    # tests creating a new account with correct values
    def testCreateAccount1(self):
        self.ui.command("login defaultuser defaultpassword")
        result0 = self.ui.command("user0 password0 Supervisor")
        self.assertEquals(result0, "User user0 has been added")
        self.ui.command("logout")

    # tests creating an account that already exists
    def testCreateAccount2(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("user1 password1 Supervisor")
        result1 = self.ui.command("user1 passwordBanana Administrator")
        self.assertEquals(result1, "user1 already exists")
        self.ui.command("logout")

    # tests creating an account when the current user has insufficient permissions
    def testCreateAccount3(self):
        self.ui.command("login defaultuser defaultpassword")
        result2 = self.ui.command("userTA passwordTA Administrator")
        self.assertEquals(result2, "You have insufficient permissions to create an account")
        self.ui.command("logout")

    # tests creating an account with invalid parameters
    def testCreateAccount4(self):
        self.ui.command("login defaultuser defaultpassword")
        result3 = self.ui.command("%$@!& .,.,.,. pumpkin")
        self.assertEquals(result3, "Account cannot be created: invalid parameter(s)")
        self.ui.command("logout")

    # tests creating an account while leaving a parameter blank
    def testCreateAccount5(self):
        self.ui.command("login defaultuser defaultpassword")
        result4 = self.ui.command("user3 password3")
        self.assertEquals(result4, "Account cannot be created: missing parameter(s)")
        self.ui.command("logout")
