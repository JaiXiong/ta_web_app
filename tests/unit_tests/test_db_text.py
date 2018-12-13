import unittest as ut
from ta_app.db_connect_object import DBConnection
from ta_app.account_object import Account
from ta_app.course_object import Course


class TestDBText(ut.TestCase):

    def setUp(self):
        self.account_correct = Account()
        self.account_correct.user = "user"
        self.account_correct.password = "password"
        self.account_correct.role = "TA"
        self.course_correct = Course()
        self.course_correct.name = "CS103"
        self.course_correct.section = "222"
        self.course_correct.days_of_week = ["M", "W", "F"]
        self.course_correct.start_time = "12:00"
        self.course_correct.end_time = "13:00"
        self.course_correct.lab_sections = "210"

    '''
        Makes sure that if the test involved creating a connection object
        that it is closed out and removed from memory each time
    '''
    def tearDown(self):
        if self.db_connection is not None and self.db_connection.db_object is not None:
            self.db_connection.db_object.close()
            self.db_connection = None

    '''
        verify that initial values were set properly
    '''
    def test_constructor(self):
        self.db_connection = DBConnection()
        self.assertFalse(self.db_connection.is_connected)
        self.assertEqual("", self.db_connection.db_path)
        self.assertIsNone(self.db_connection.db_object)

    '''
        verify that the members are set properly after a successful connection
    '''
    def test_connectSuccessful(self):
        temp_db_path = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path))
        self.assertTrue(self.db_connection.is_connected)
        self.assertEqual(temp_db_path, self.db_connection.db_path)
        self.assertIsNotNone(self.db_connection.db_object)

    '''
        If a file is passed that doesn't exist the function will return false
        The members also will not update and should appear the same as after construction
    '''
    def test_connect_Unsuccessful(self):
        temp_db_path = "notreal.csv"
        self.db_connection = DBConnection()
        self.assertFalse(self.db_connection.connect(temp_db_path))
        self.assertFalse(self.db_connection.is_connected)
        self.assertEqual("", self.db_connection.db_path)
        self.assertIsNone(self.db_connection.db_object)

    '''
        Verifies that the members are properly set after a disconnect from a DB
    '''
    def test_disconnect_Successful(self):
        temp_db_path = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path))
        self.assertTrue(self.db_connection.disconnect())
        self.assertFalse(self.db_connection.is_connected)
        self.assertEqual("", self.db_connection.db_path)
        self.assertIsNone(self.db_connection.db_object)

    '''
        Verifies that the you can only disconnect a connected object,
        and that members reflect an unconnected connection object
    '''
    def test_disconnect_Unsuccessful(self):
        self.db_connection = DBConnection()
        self.assertFalse(self.db_connection.disconnect())
        self.assertFalse(self.db_connection.is_connected)
        self.assertEqual("", self.db_connection.db_path)
        self.assertIsNone(self.db_connection.db_object)

    '''
        Verifies that if given a valid DB filepath, and a valid account object,
        add_account should return true and you should be able to see the account in the file
    '''
    def test_add_account_Successful(self):
        temp_db_path_correct = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path_correct))
        self.assertTrue(self.db_connection.is_connected)
        self.assertEqual(temp_db_path_correct, self.db_connection.db_path)
        self.assertTrue(self.db_connection.add_account(self.account_correct))

    '''
        Verifies that if any null object is passed into the function it will return false,
        and that the members will not have updated to a successful state
    '''
    def test_add_account_None(self):
        temp_db_path_correct = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path_correct))
        self.assertTrue(self.db_connection.is_connected)
        self.assertEqual(temp_db_path_correct, self.db_connection.db_path)
        self.assertFalse(self.db_connection.add_account(None))

    '''
        Verifies that if given a successful filepath and an account that is in the DB it removes it,
        and returns true
    '''
    def test_remove_account_Successful(self):
        temp_db_path_correct = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path_correct))
        self.assertTrue(self.db_connection.is_connected)
        self.assertEqual(temp_db_path_correct, self.db_connection.db_path)
        self.assertTrue(self.db_connection.add_account(self.account_correct))
        self.assertTrue(self.db_connection.remove_account(self.account_correct))

    '''
        Verifies that if any null object is passed into the function it will return false,
        and that the members will not have updated to a successful state
    '''
    def test_remove_account_None(self):
        temp_db_path_correct = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path_correct))
        self.assertTrue(self.db_connection.is_connected)
        self.assertEqual(temp_db_path_correct, self.db_connection.db_path)
        self.assertTrue(self.db_connection.add_account(self.account_correct))
        self.assertFalse(self.db_connection.remove_account(None))

    '''
        Verifies that the function will only return true if the account to delete is
        in the database, otherwise it returns false
    '''
    def test_remove_account_NoExistAccount(self):
        temp_db_path_correct = "C:/Users/Admin/PycharmProjects/ta_app/DB_Files/accounts.csv"
        account2 = Account()
        account2.user = "user2"
        account2.password = "pass2"
        account2.role = "TA"
        self.db_connection = DBConnection()
        self.assertTrue(self.db_connection.connect(temp_db_path_correct))
        self.assertTrue(self.db_connection.is_connected)
        self.assertEqual(temp_db_path_correct, self.db_connection.db_path)
        self.assertTrue(self.db_connection.add_account(self.account_correct))
        self.assertFalse(self.db_connection.remove_account(account2))
