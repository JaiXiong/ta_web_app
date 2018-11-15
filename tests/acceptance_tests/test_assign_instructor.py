import unittest as ut
from ui import self


class Test_assign_instructor(ut.TestCase):

    def setUp(self):
        self.ui = self()

    def test_AddCourse (self):
        self.ui.input_command("create_account user1 user1pass instructor")
        self.ui.input_command("create_account user2 user2pass supervisor")
        self.ui.input_command("login user2 user2pass")
        self.assertEqual(self.ui.input_command("assign_instructor user1 cs101"),
                         "user1 has been added to cs101")

    def test_Overlap(self):
        self.ui.input_command("create_account user1 user1pass instructor")
        self.ui.input_command("create_account user2 user2pass supervisor")
        self.ui.input_command("login user2 user2pass")
        self.ui.input_command("assign_instructor user1 cs101")
        self.assertEqual(self.ui.input_command("assign_instructor user1 cs102"),
                         "user1 has a timing conflict with cs102")

    def test_NoPermissions(self):
        self.ui.input_command("create_account user1 user1pass instructor")
        self.ui.input_command("create_account user2 user2pass supervisor")
        self.ui.input_command("login user1 user1pass")
        self.assertEqual(self.ui.input_command("assign_instructor cs101"), "Current user has insufficient permissions")