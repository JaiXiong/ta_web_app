import unittest as ut
from ta_app.ui import UI
from ta_app.account_object import Account
from ta_app.superuser_login import Superuser


class TestSuperuserLogin(ut.TestCase):

    # set up default username, password, role
    # sets up a basic account with superuser defaults
    def setUp(self):
        self.super = Superuser()
        self.user = Account()
        self.ui = UI()
        self.user.set_user = "default_superuser"
        self.user.set_password = "default_password"
        self.user.set_role = "default_superuser"

    # check login with default username/password
    def test_defaultLogin(self):
        response = "logged in as default_superuser"
        self.ui.command("login default_superuser default_password")
        self.assertEqual(response, self.super.superuser_authentication("default_superuser", "default_password"))

    # check login with right username, wrong password
    def test_wrongLogin(self):
        response = "login failed. Invalid username or password"
        self.ui.command("login default_superuser wrong_password")
        self.assertEqual(response, self.super.superuser_authentication("default_superuser", "new_password"))

    # check login with wrong username, right password
    def test_wrongLogin2(self):
        response = "login failed. Invalid username or password"
        self.ui.command("login wrong_superuser default_password")
        self.assertEqual(response, self.super.superuser_authentication("new_superuser", "default_password"))

    # check login when nothing entered
    def test_enterNothing(self):
        response = "login failed. Invalid username or password"
        self.assertEqual(response, self.super.superuser_authentication("", ""))

    # check login when role of superuser for any reason is not 'superuser'
    # makes call to Superuser check_role, checks wrong condition
    def test_wrongRole(self):
        self.assertFalse(self.super.check_role("supervisor"))

    # check login when role of superuser is superuser
    # makes call to Superuser check_role, checks right condition
    def test_rightRole(self):
        self.assertTrue(self.super.check_role("default_superuser"))

    # check login when username entered is wrong
    # makes call to Superuser check_name, checks wrong condition
    def test_wrongName(self):
        self.user.set_role = "new_superuser"
        self.assertFalse(self.super.check_name("new_superuser"))

    # check login when username entered is correct
    # makes call to Superuser check_name, checks right condition
    def test_rightName(self):
        self.assertTrue(self.super.check_name("default_superuser"))

    # check login when password is entered wrong
    # makes call to Superuser check_password, checks wrong condition
    def test_wrongPass(self):
        self.user.set_password = "new_password"
        self.assertFalse(self.super.check_password("new_password"))

    # check login when password is entered correct
    # makes call to Superuser check_password, checks right condition
    def test_rightPass(self):
        self.assertTrue(self.super.check_password("default_password"))
