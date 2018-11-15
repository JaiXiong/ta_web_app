import unittest as ut
from ui import self


class TestEditContactInfo(ut.TestCase):

    def setUp(self):
        self.ui = self()

    def testValidEditPhoneNumber(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("phonenumber (555)423-5980")
        self.assertEqual(output, "user1 (555)423-5980 "" """)
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testInvalidEditPhoneNumber(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("phonenumber (5")
        self.assertEqual(output, "That is not a valid input for phonenumber")
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testValidEditEmail(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("email user1@uwm.edu")
        self.assertEqual(output, "user1 "" user1@uwm.edu """)
        self.assertTrue(output)
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testInvalidEditEmail(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("email user1&uwm.edu")
        self.assertEqual(output, "That is not a valid input for email")
        self.assertTrue(output)
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testValidEditAddress(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("address 123 Drive Milwaukee, WI 53211")
        self.assertEqual(output, "user1 "" "" 123 Drive Milwaukee, WI 53211")
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testInvalidEditAddress(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("address 123")
        self.assertEqual(output, "That is not a valid input for address")
        self.ui.command("delete_account user1")
        self.ui.command("logout")

    def testInvalidField(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_account user1 pass1 TA")
        output = self.ui.command("edit_account_info user1")
        self.assertEqual(output, "user1 "" "" """)
        output = self.ui.command("grades 123")
        self.assertEqual(output, "That is not a valid field")
        self.ui.command("delete_account user1")
        self.ui.command("logout")
