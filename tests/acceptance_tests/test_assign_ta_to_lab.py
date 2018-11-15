import unittest as ut
from ui import self


class TestAssignTaToLab(ut.TestCase):

    def setUp(self):
        self.ui = self()

    def testSuccessfulAssign(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_user user1 pass1 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        output = self.ui.command("assign_ta_to_lab user1 BS101 906")
        self.assertEqual(output, "user1 has been added to 906")
        self.ui.command("delete_user user1")
        self.ui.command("logout")

    def testSuccessfulDoubleAssign(self): #do we allow TAs multiple lab sections?
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_user user1 pass1 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        self.ui.command("create_course BS102 421 R 4:00PM-4:50PM 909")
        output = self.ui.command("assign_ta_to_lab user1 BS101 906")
        self.assertEqual(output, "user1 has been added to 906")
        output = self.ui.command("assign_ta_to_lab user1 BS102 909")
        self.assertEqual(output, "user1 has been added to 909")
        self.ui.command("delete_user user1")
        self.ui.command("logout")

    def testConflictingAssign(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_user user1 pass1 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        self.ui.command("create_course ED233 421 M/W/F 9:00AM-9:50PM 909")
        self.ui.command("assign_ta_to_lab user1 BS101 906")
        output = self.ui.command("assign_ta_to_lab user1 ED233 909")
        self.assertEqual(output, "user1 has a timing conflict with this assignment")

    def testPermissionToAssign(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        self.ui.command("create_account user2 pass2 TA")
        self.ui.command("create_course BS101 420 M/W/F 9:00AM-9:50AM 906")
        self.ui.command("logout")
        self.ui.command("login user2 pass2")
        output = self.ui.command("assign_ta_to_lab user1 BS102 906")
        self.assertEqual(output, "You do not have permissions to assign TAs to lab sections")
        self.ui.command("logout")
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("delete_user user1")
        self.ui.command("delete_user user2")
        self.ui.command("logout")
