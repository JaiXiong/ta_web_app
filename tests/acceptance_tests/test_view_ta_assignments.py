# Joe Connelly
import unittest as ut
from ui import self


class TestViewTaAssignments(ut.TestCase):

    def setUp(self):
        self.ui = self()
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account Prof0 pass0 Instructor")
        self.ui.command("create_account ta0 pass1 TA")
        self.ui.command("create_account ta1 pass2 TA")
        self.ui.command("create_course CS361 401 TH 1100-1200 801/802")
        self.ui.command("assign_ta_to_course ta0 CS361")
        self.ui.command("assign_ta_to_course ta1 CS361")
        self.ui.command("assign_ta_to_lab ta0 CS361 801")
        self.ui.command("assign_ta_to_lab ta1 CS361 802")
        self.expectedResult = "ta0 CS361 801\n" \
                              "ta1 CS361 802"
        self.ui.command("logout")

    def tearDown(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("delete_account Prof0")
        self.ui.command("delete_account ta0")
        self.ui.command("delete_account ta1")
        self.ui.command("logout")

    def testViewAsInstructor(self):
        self.ui.command("login Prof0 pass0")
        actualResult = self.ui.command("view_ta_assignments")
        self.assertEqual(self.expectedResult, actualResult)
        self.ui.command("logout")

    def testViewAsTA(self):
        self.ui.command("login ta0 pass1")
        actualResult = self.ui.command("view_ta_assignments")
        self.assertEqual(self.expectedResult, actualResult)
        self.ui.command("logout")
