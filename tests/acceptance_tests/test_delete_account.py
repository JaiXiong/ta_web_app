import unittest as ut
from ta_app.ui import UI


class TestDeleteAccount(ut.TestCase):

    def setUp(self):
        self.ui = UI()
        self.ui.command("create_account defaultuser defaultpassword Supervisor")

    # test correctly deleting an account
    def testDeleteAccount(self):
        result1 = self.ui.command("delete_account defaultuser")
        self.assertEqual(result1, "defaultuser has been removed")

    # test deleting an account that does not exist
    def testDeleteAccount2(self):
        result2 = self.ui.command("delete_account cabbage")
        self.assertEqual(result2, "cabbage does not exist")

    # test deleting an account when that account is assigned to a course
    def testDeleteAccount3(self):
        pass

