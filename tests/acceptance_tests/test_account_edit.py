import unittest as ut
from ta_app.ui import UI


class Test_account_edit(ut.TestCase):

    def setUp(self):
        self.ui = UI()

    # test if username exist when not yet created
    def test_notExist(self):
        self.ui.command("login user1 user1pass")
        self.ui.command("edit_account user2")
        self.assertEqual(self.ui.command("edit_account user2"), "user2 doesn't exist")

    # test 2 different permissions
    def test_permissions(self):
        self.ui.command("create_account user1 user1pass instructor")
        self.ui.command("create_account user2 user2pass ta")
        self.ui.command("login user2 user2pass")
        self.assertEqual(self.ui.command("edit_account user1"), "you don't have permissions to edit this user")

    # test the view of the permissions based on login user
    def test_viewPermission(self):
        permissionList = "create_course\n" \
                         "create_account\n" \
                         "delete_account\n" \
                         "edit_account\n" \
                         "send_notification\n" \
                         "access_data\n" \
                         "assign_instructor\n" \
                         "assign_TA\n" \
                         "assign_lab\n"
        self.ui.command("create_account user1 user1pass supervisor")
        self.ui.command("create_account user2 user2pass ta")
        self.ui.command("login user1 user1pass")
        self.assertEqual(permissionList, self.ui.command("edit_account user2"))
        self.assertEqual("please specify what field you would like to change "
                         "and it's new value", self.ui.command("edit_account user2"))

    # test the correct type is entered after selection of field
    def test_type(self):
        self.ui.command("create_account user1 user1pass supervisor")
        self.ui.command("create_account user2 user2pass ta")
        self.ui.command("login user1 user1pass")
        self.ui.command("edit_account user2")
        self.assertEqual(self.ui.command("<password> .....,.,.,,..,`````"),
                         "Entered value is not valid for <password>")

    # test that the field is correct to begin with
    def test_type2(self):
        self.ui.command("create_account user1 user1pass supervisor")
        self.ui.command("create_account user2 user2pass ta")
        self.ui.command("login user1 user1pass")
        self.ui.command("edit_account user2")
        self.ui.command("<gibberish> ......,,,......")
        self.assertEqual(self.ui.command("<gibberish>"),
                         "Entered field <gibberish> is not valid field")