import unittest as ut
from ui import self


class TestLogout(ut.TestCase):

    def setUp(self):
        self.uio = self()
        self.uio.command("create_account Bob bobspw Supervisor")

    # Successful logout of current user
    def test_logout1(self):
        self.uio.command("login Bob bobspw")
        response = self.uio.command("logout")
        self.assertEqual(response, "Bob has been logged out.")
        self.assertNotEqual(self.uio.currentUser, "Bob")

    # Make sure current user isn't changed if no one is logged in
    def test_logout2(self):
        self.assertEqual(self.uio.currentUser, "")
        self.uio.command("logout")
        self.assertEqual(self.uio.currentUser, "")