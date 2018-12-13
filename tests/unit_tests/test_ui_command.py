import unittest as ut
from unittest import mock
from ta_app.ui import UI


class TestUiCommand(ut.TestCase):

    def setUp(self):
        self.uio = UI()

    # check that "help" is being called with no parameters
    def test_UiCommand1(self):
        patcher = mock.patch.object(self, "help")
        patched = patcher.start()
        self.uio.command("help")
        assert patched.call_count == 1
        patched.assert_called_with()

    # check that "connect_db" is being called by ui.command("connect_db")
    def test_UiCommand2(self):
        pass

    # check that "disconnect_db" is being called by ui.command("disconnect_db")
    def test_UiCommand3(self):
        pass

    # check that "login" is being called with  parameters "username" "password"
    def test_UiCommand4(self):
        patcher = mock.patch.object(self, "login")
        patched = patcher.start()
        self.uio.command("login username password")
        assert patched.call_count == 1
        patched.assert_called_with("username", "password")

    # check that "logout" is called with no parameters
    def test_UiCommand5(self):
        patcher = mock.patch.object(self, "logout")
        patched = patcher.start()
        self.uio.command("logout")
        assert patched.call_count == 1
        patched.assert_called_with()

    # check that "create_course" is called with "coursename" "section" daysofweek" "time" "labsec"
    def test_UiCommand6(self):
        patcher = mock.patch.object(self, "create_course")
        patched = patcher.start()
        self.uio.command("create_course coursename section daysofweek time labsec")
        assert patched.call_count == 1
        patched.assert_called_with("coursename", "section", "daysofweek", "time", "labsec")

    # check that "create_account" is called with "username" "password" "role"
    def test_UiCommand7(self):
        patcher = mock.patch.object(self, "create_account")
        patched = patcher.start()
        self.uio.command("create_account username password role")
        assert patched.call_count == 1
        patched.assert_called_with("username", "password", "role")

    # check that "delete_account" is called with "username"
    def test_UiCommand8(self):
        patcher = mock.patch.object(self, "delete_account")
        patched = patcher.start()
        self.uio.command("delete_account username")
        assert patched.call_count == 1
        patched.assert_called_with("username")

    # check that "edit_account" is called with "username"
    def test_UiCommand9(self):
        patcher = mock.patch.object(self, "edit_account")
        patched = patcher.start()
        self.uio.command("edit_account username")
        assert patched.call_count == 1
        patched.assert_called_with("username")

    # check that "assign_instructor" is called with "username" "coursename"
    def test_UiCommand10(self):
        patcher = mock.patch.object(self, "assign_instructor")
        patched = patcher.start()
        self.uio.command("assign_instructor username coursename")
        assert patched.call_count == 1
        patched.assert_called_with("username", "coursename")

    # check that "assign_ta_to_course" is called with "username" "coursename"
    def test_UiCommand11(self):
        patcher = mock.patch.object(self, "assign_ta_to_course")
        patched = patcher.start()
        self.uio.command("assign_ta_to_course username coursename")
        assert patched.call_count == 1
        patched.assert_called_with("username", "coursename")

    # check that "assign_ta_to_lab" is called with "username" "coursename" "labsec"
    def test_UiCommand12(self):
        patcher = mock.patch.object(self, "assign_ta_to_lab")
        patched = patcher.start()
        self.uio.command("assign_ta_to_lab username coursename labsec")
        assert patched.call_count == 1
        patched.assert_called_with("username", "coursename", "labsec")

    # check that "edit_contact_info" is called with no parameters
    def test_UiCommand13(self):
        patcher = mock.patch.object(self, "edit_contact_info")
        patched = patcher.start()
        self.uio.command("edit_contact_info")
        assert patched.call_count == 1
        patched.assert_called_with()

    # check that "view_course_assignments" is called with no parameters
    def test_UiCommand14(self):
        patcher = mock.patch.object(self, "view_course_assignments")
        patched = patcher.start()
        self.uio.command("view_course_assignments")
        assert patched.call_count == 1
        patched.assert_called_with()

    # check that "view_ta_assignments" is called with no parameters
    def test_UiCommand15(self):
        patcher = mock.patch.object(self, "view_ta_assignments")
        patched = patcher.start()
        self.uio.command("view_ta_assignments")
        assert patched.call_count == 1
        patched.assert_called_with()

    # check that "read_contact_info" is called with no parameters
    def test_UiCommand16(self):
        patcher = mock.patch.object(self, "read_contact_info")
        patched = patcher.start()
        self.uio.command("read_contact_info")
        assert patched.call_count == 1
        patched.assert_called_with()

    # check that Error is thrown when invalid parameters are passed
    def test_UiCommand17(self):
        response = self.uio.command("notacommand")
        self.assertEqual(response, "ERROR: this is not an available command")

    # check that not passing the proper parameters still passes to the method
    def test_UiCommand18(self):
        patcher = mock.patch.object(self, "login")
        patched = patcher.start()
        self.uio.command("login username")
        assert patched.call_count == 1
        patched.assert_called_with("username")

    # check that passing extra parameters still calls "login"
    def test_UiCommand19(self):
        patcher = mock.patch.object(self, "login")
        patched = patcher.start()
        self.uio.command("login username password role")
        assert patched.call_count == 1
        patched.assert_called_with("username", "password", "role")