import unittest as ut
from ta_app.ui import UI


# All tests will not pass until permissions are complete
class TestHelp(ut.TestCase):

    def setUp(self):
        self.uio = UI()
        self.uio.command("create_account Bob bobspw Supervisor")
        self.uio.command("create_account Alice alicespw Administrator")
        self.uio.command("create_account Eve evespw Instructor")
        self.uio.command("Create_account Adam adamspw TA")

    # Test help with no current user
    def test_help1(self):
        self.assertEqual(self.uio.currentUser, "")
        response = self.uio.command("help")
        self.assertEqual(response, "Please login.")

    # Test help with Supervisor permissions
    def test_help2(self):
        supervisorhelpstring = "create_course <name> <section> <days_of_week> <times> (<lab sections>)\n" \
                           "create_account <username> <password> <role>\n" \
                           "delete_account <username>\n" \
                           "edit_account <username>\n" \
                           "assign_instructor <username> <course>\n" \
                           "assign_ta_to_course <username> <course>\n" \
                           "assign_ta_to_lab <username> <course> <labsection>\n" \
                           "send_notification <username>\n" \
                           "access_system_data"

        self.uio.command("login Bob bobspw")
        response = self.uio.command("help")
        self.assertEqual(response, supervisorhelpstring)

    # Test help with Administrator permissions
    def test_help3(self):
        administratorhelpstring = "create_course <name> <section> <days_of_week> <times> (<lab sections>)\n" \
                           "create_account <username> <password> <role>\n" \
                           "delete_account <username>\n" \
                           "edit_account <username>\n" \
                           "send_notification <username>\n" \
                           "access_system_data"

        self.uio.command("login Alice alicespw")
        response = self.uio.command("help")
        self.assertEqual(response, administratorhelpstring)

    # Test help with Instructor permissions
    def test_help4(self):
        instructorhelpstring = "edit_contact_info\n" \
                            "view_course_assignments\n" \
                            "view_ta_assignments\n" \
                            "assign_ta_to_lab <username> <course> <labsection>\n" \
                            "send_notification <username>\n" \
                            "read_contact_info"

        self.uio.command("login Eve evespw")
        response = self.uio.command("help")
        self.assertEqual(response, instructorhelpstring)

    # Test help with Instructor permissions
    def test_help5(self):
        tahelpstring = "edit_contact_info\n" \
                    "view_course_assignments\n" \
                    "view_ta_assignments\n" \
                    "read_contact_info"

        self.uio.command("login Adam adamspw")
        response = self.uio.command("help")
        self.assertEqual(response, tahelpstring)