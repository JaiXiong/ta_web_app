# Joe Connelly
import unittest as ut
from ui import self


class TestViewCourseAssignments(ut.TestCase):

    def setUp(self):
        self.ui = self()
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account Prof0 pass0 Instructor")
        self.ui.command("create_account Prof1 pass1 Instructor")
        self.ui.command("create_account ta0 pass2 TA")
        self.ui.command("create_course CS361 401 TH 1100-1200 801")
        self.ui.command("create_course CS337 401 MWF 0900-1000 801")
        self.ui.command("create_course CS317 401 MW 1300-1415")
        self.ui.command("assign_instructor Prof0 CS361")
        self.ui.command("assign_instructor Prof0 CS337")
        self.ui.command("assign_instructor Prof1 CS317")
        self.ui.command("logout")

    def tearDown(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("delete_account Prof0")
        self.ui.command("delete_account Prof1")
        self.ui.command("delete_account ta0")
        self.ui.command("logout")

    def testViewAsInstructor1(self):
        self.ui.command("login Prof0 pass0")
        expectedResult = "CS361 401 TH 1100-1200 801\n" \
                         "CS337 401 MWF 0900-1000 801"
        actualResult = self.ui.command("view_course_assignments")
        self.assertEqual(expectedResult, actualResult)
        self.ui.command("logout")

    def testViewAsInstructor2(self):
        self.ui.command("login Prof1 pass1")
        expectedResult = "CS317 401 MW 1300-1415"
        actualResult = self.ui.command("view_course_assignments")
        self.assertEqual(expectedResult, actualResult)
        self.ui.command("logout")

    def testViewAsTA(self):
        self.ui.command("login ta0 pass2")
        expectedResult = "Insufficient permissions"
        actualResult = self.ui.command("view_course_assignments")
        self.assertEqual(expectedResult, actualResult)
        self.ui.command("logout")
