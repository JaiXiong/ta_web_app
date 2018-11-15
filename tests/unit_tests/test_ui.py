import unittest as ut
from ta_app.ui import UI


class TestUI(ut.TestCase):

    def setUp(self):
        self.ui = UI()
        self.ui.sCurrentUser = 'default_superuser'

    def test_connect_db_failed(self):
        empty_path = ''
        invalid_path = 'C:/invalidpath.csv'
        result1 = self.ui.connect_db(empty_path)
        result2 = self.ui.connect_db(invalid_path)
        self. assertFalse(result1.is_connected)
        self.assertFalse(result2.is_connected)

    def test_connect_db_successful(self):
        result_connect_accounts = self.ui.connect_db('C:/Users/user/PycharmProjects/ta_app/DB_Files/accounts.csv')
        result_connect_courses = self.ui.connect_db('C:/Users/user/PycharmProjects/ta_app/DB_Files/courses.csv')
        self. assertTrue(result_connect_accounts.is_connected)
        self.assertTrue(result_connect_courses.is_connected)

    # test is for super user only as of now
    def test_login_success(self):
        result = self.ui.login('default_superuser', 'default_password')
        self.assertEqual(result, 'login successful...')
        self.assertEqual(self.ui.sCurrentUser, 'default_superuser')

    def test_login_badUser(self):
        self.ui.sCurrentUser = ''
        result = self.ui.login('badUser', 'default_password')
        self.assertEqual(result, 'login failed! bad username/ password')
        self.assertEqual(self.ui.sCurrentUser, '')

    def test_login_badPassword(self):
        self.ui.sCurrentUser = ''
        result = self.ui.login('default_superuser', 'badPassword')
        self.assertEqual(result, 'login failed! bad username/ password')
        self.assertEqual(self.ui.sCurrentUser, '')

    def test_logout(self):
        self.ui.sCurrentUser = 'default_superuser'
        result = self.ui.logout()
        self.assertEqual(result, 'logout successful...')
        self.assertEqual(self.ui.sCurrentUser, '')

    def test_create_account_success(self):
        self.ui.sCurrentUser = 'default_superuser'
        result = self.ui.create_account('user', 'pass', 'TA')
        self.assertEqual(result, 'Successfully created account')

    def test_create_account_failed_bad_arg(self):
        self.ui.sCurrentUser = 'default_superuser'
        result_no_pass = self.ui.create_account('user', '', 'role')
        result_no_user = self.ui.create_account('', 'password', 'role')
        result_no_role = self.ui.create_account('user', 'password', '')
        self.assertEqual(result_no_pass, 'Failed to create account. Invalid or missing argument')
        self.assertEqual(result_no_user, 'Failed to create account. Invalid or missing argument')
        self.assertEqual(result_no_role, 'Failed to create account. Invalid or missing argument')

    def test_create_account_failed_insufficient_permissions(self):
        self.ui.sCurrentUser = 'user'
        result = self.ui.create_account('user', 'pass', 'role')
        self.assertEqual(result, 'Failed to create account. Insufficient permissions')

    def test_create_course_failed_insufficient_permissions(self):
        self.ui.sCurrentUser = 'user'
        result = self.ui.create_course("CS-337", "004", "M/W/F", "11:00-11:50", "001/002/003")
        self.assertEqual(result, 'Failed to create course. Insufficient permissions')

    def test_create_course_failed_missing_arguments(self):
        self.ui.sCurrentUser = 'default_superuser'
        result1 = self.ui.create_course("", "004", "M/W/F", "11:00-11:50", "001/002/003")
        result2 = self.ui.create_course("CS-337", "", "M/W/F", "11:00-11:50", "001/002/003")
        result3 = self.ui.create_course("CS-337", "004", "", "11:00-11:50", "001/002/003")
        result4 = self.ui.create_course("CS-337", "004", "M/W/F", "", "001/002/003")
        result5 = self.ui.create_course("CS-337", "004", "M/W/F", "11:00-11:50", "")
        self.assertEqual(result1, 'Failed to create course. Invalid arguments')
        self.assertEqual(result2, 'Failed to create course. Invalid arguments')
        self.assertEqual(result3, 'Failed to create course. Invalid arguments')
        self.assertEqual(result4, 'Failed to create course. Invalid arguments')
        self.assertEqual(result5, 'Failed to create course. Invalid arguments')

    def test_create_course_success(self):
        self.ui.sCurrentUser = 'default_superuser'
        result = self.ui.create_course("CS-337", "004", "M/W/F", "11:00-11:50", "001/002/003")
        self.assertEqual(result, 'Course created successfully')

    def test_delete_account_successful(self):
        self.ui.sCurrentUser = 'default_superuser'
        self.ui.create_account('user', 'pass', 'TA')
        result = self.ui.delete_account('user', 'pass', 'TA')
        self.assertEqual(result, 'Successfully deleted account')

    def test_delete_account_failed_missing_argument(self):
        self.ui.sCurrentUser = 'default_superuser'
        result = self.ui.delete_account('')
        self.assertEqual(result, 'Failed to delete account. Invalid or missing argument')

    def test_delete_account_failed_insufficient_permissions(self):
        self.ui.sCurrentUser = 'user'
        self.ui.create_account('user1', 'pass', 'TA')
        result = self.ui.delete_account('user', 'pass', 'TA')
        self.assertEqual(result, 'Failed to delete account. Insufficient permissions')

    def test_delete_account_failed_UserNotExist(self):
        self.ui.sCurrentUser = 'default_superuser'
        result = self.ui.delete_account('UserNotExist', 'pass', 'TA')
        self.assertEqual(result, 'Failed to delete account. User not found')




