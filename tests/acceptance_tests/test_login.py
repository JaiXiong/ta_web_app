import unittest as ut
from ui import self


class TestLogin(ut.TestCase):

    def setUp(self):
        self.uio = self()
        self.uio.command("create_account Bob bobspw Supervisor")

    def tearDown(self):
        self.uio.command("delete Bob")

    # Successful login of user in database
    def test_login1(self):
        response = self.uio.command("login Bob bobspw")
        self.assertEqual(response, "Logged in as Bob.")
        self.assertEqual(self.uio.currentUser, "Bob")

    # Failed login, user not in data base
    def test_login2(self):
        response = self.uio.command("login Alice alicespw")
        self.assertEqual(response, "Login failed. Invalid username or password.")
        self.assertNotEqual(self.uio.currentUser, "Alice")

    # Failed login, password is incorrect
    def test_login3(self):
        response = self.uio.command("login Bob notbobspw")
        self.assertEqual(response, "Login failed. Invalid username or password.")
        self.assertNotEqual(self.uio.currentUser, "Bob")