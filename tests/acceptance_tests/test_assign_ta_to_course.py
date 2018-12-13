import unittest as ut
from ta_app.ui import UI


class TestAssignTaToCourse(ut.TestCase):

    def setUp(self):
        self.ui = UI()

    def testSuccessfulAssign(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        output = self.ui.command("assign_ta_to_course user1 BS101")
        self.assertEqual(output, "user1 has been added to BS101")
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testConflictingAssignment(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        self.ui.command("create_course BS102 421 T/H 4:00PM-4:50PM 909")
        output = self.ui.command("assign_ta_to_course user1 BS102")
        self.assertEqual(output, "user1 is already assigned to a course")
        self.ui.command("delete_user user1")
        self.ui.command("logout")

    def testPermissionToAssign(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        self.ui.command("create_account user2 pass2 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        self.ui.command("logout")
        self.ui.command("login user2 pass2")
        output = self.ui.command("assign_ta_to_course user1 BS102")
        self.assertEqual(output, "You do not have permissions to assign TAs to courses")
        self.ui.command("logout")
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("delete_user user1")
        self.ui.command("delete_user user2")
        self.ui.command("logout")
