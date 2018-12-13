import unittest as ut
from ta_app.ui import UI


class Test_assign_instructor(ut.TestCase):

    def setUp(self):
        self.ui = UI()

    def test_AddCourse(self):
        self.ui.command("create_account user1 user1pass instructor")
        self.ui.command("create_account user2 user2pass supervisor")
        self.ui.command("login user2 user2pass")
        self.assertEqual(self.ui.command("assign_instructor user1 cs101"),
                         "user1 has been added to cs101")

    def test_Overlap(self):
        self.ui.command("create_account user1 user1pass instructor")
        self.ui.command("create_account user2 user2pass supervisor")
        self.ui.command("login user2 user2pass")
        self.ui.command("assign_instructor user1 cs101")
        self.assertEqual(self.ui.command("assign_instructor user1 cs102"),
                         "user1 has a timing conflict with cs102")

    def test_NoPermissions(self):
        self.ui.command("create_account user1 user1pass instructor")
        self.ui.command("create_account user2 user2pass supervisor")
        self.ui.command("login user1 user1pass")
        self.assertEqual(self.ui.command("assign_instructor cs101"), "Current user has insufficient permissions")