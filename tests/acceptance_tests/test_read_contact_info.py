# Joe Connelly
import unittest as ut
from ui import self


class TestReadContactInfo(ut.TestCase):

    def setUp(self):
        self.ui = self()
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account Prof0 pass0 Instructor")
        self.ui.command("create_account ta0 pass1 TA")
        self.ui.command("create_account ta1 pass2 TA")
        self.ui.command("logout")

        self.ui.command("login Prof0 pass0")
        self.ui.command("edit_contact_info")
        self.ui.command("phonenumber 414-388-4500")
        self.ui.command("email Prof@uwm.edu")
        self.ui.command("address 3523 S Howell Ave Milwaukee WI 53221")
        self.ui.command("logout")

        self.ui.command("login ta0 pass1")
        self.ui.command("edit_contact_info")
        self.ui.command("phonenumber 414-545-3661")
        self.ui.command("email ta@uwm.edu")
        self.ui.command("logout")

        self.expectedResult = "Prof 414-388-4500 Prof@uwm.edu 3523 S Howell Ave Milwaukee WI 53221\n" \
                              "ta0 414-545-3661 ta@uwm.edu"

    def tearDown(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("delete_account Prof")
        self.ui.command("delete_account ta0")
        self.ui.command("delete_account ta1")
        self.ui.command("logout")

    def testViewAsInstructor(self):
        self.ui.command("login Prof0 pass0")
        actualResult = self.ui.command("read_contact_info")
        self.assertEqual(self.expectedResult, actualResult)
        self.ui.command("logout")

    def testViewAsTA(self):
        self.ui.command("login ta0 pass1")
        actualResult = self.ui.command("read_contact_info")
        self.assertEqual(self.expectedResult, actualResult)
        self.ui.command("logout")
