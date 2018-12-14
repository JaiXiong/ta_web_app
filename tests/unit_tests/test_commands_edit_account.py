from django.test import TestCase
from ta_app.commands import Commands
import ta_app.wsgi
from website.models import Account


class TestEditAccount(TestCase):

    def setUp(self):
        self.ui = Commands()
        self.tst_supervisor = Account(user='usrSupervisor', password='password', role='Supervisor')
        self.tst_administrator = Account(user='usrAdministrator', password='password', role='Administrator')
        self.tst_instructor = Account(user='usrInstructor', password='password', role='Instructor')
        self.tst_ta = Account(user='usrTA', password='password', role='TA')
        self.tst_supervisor.save()
        self.tst_administrator.save()
        self.tst_instructor.save()
        self.tst_ta.save()

    def test_no_current_user(self):
        self.ui.current_user = Account()
        new_phone = '414-368-6425'
        expected_output = 'Failed to edit account. Insufficient permissions'
        actual_output = self.ui.edit_account(self.tst_ta.user, phone_number=new_phone)
        self.assertEqual(expected_output, actual_output)

    def test_edit_account_as_ta(self):
        self.ui.current_user = self.tst_ta
        new_phone = '414-368-6425'
        expected_output = 'Failed to edit account. Insufficient permissions'
        actual_output1 = self.ui.edit_account(self.tst_ta.user, phone_number=new_phone)
        actual_output2 = self.ui.edit_account(self.tst_instructor, phone_number=new_phone)
        actual_output3 = self.ui.edit_account(self.tst_administrator, phone_number=new_phone)
        actual_output4 = self.ui.edit_account(self.tst_supervisor, phone_number=new_phone)
        self.assertEqual(expected_output, actual_output1)
        self.assertEqual(expected_output, actual_output2)
        self.assertEqual(expected_output, actual_output3)
        self.assertEqual(expected_output, actual_output4)

    def test_edit_account_as_instructor(self):
        self.ui.current_user = self.tst_instructor
        new_phone = '414-368-6425'
        expected_output = 'Failed to edit account. Insufficient permissions'
        actual_output1 = self.ui.edit_account(self.tst_ta.user, phone_number=new_phone)
        actual_output2 = self.ui.edit_account(self.tst_instructor, phone_number=new_phone)
        actual_output3 = self.ui.edit_account(self.tst_administrator, phone_number=new_phone)
        actual_output4 = self.ui.edit_account(self.tst_supervisor, phone_number=new_phone)
        self.assertEqual(expected_output, actual_output1)
        self.assertEqual(expected_output, actual_output2)
        self.assertEqual(expected_output, actual_output3)
        self.assertEqual(expected_output, actual_output4)

    def test_edit_supervisor_account_as_administrator(self):
        self.ui.current_user = self.tst_administrator
        new_phone = '414-368-6425'
        expected_output = 'Failed to edit account. Insufficient permissions'
        actual_output = self.ui.edit_account(self.tst_supervisor.user, phone_number=new_phone)
        self.assertEqual(expected_output, actual_output)

    def test_edit_account_as_administrator(self):
        self.ui.current_user = self.tst_administrator
        new_phone = '414-368-6425'
        expected_output = 'Account updated'
        actual_output1 = self.ui.edit_account(self.tst_ta.user, phone_number=new_phone)
        actual_output2 = self.ui.edit_account(self.tst_instructor.user, phone_number=new_phone)
        actual_output3 = self.ui.edit_account(self.tst_administrator.user, phone_number=new_phone)
        self.assertEqual(expected_output, actual_output1)
        self.assertEqual(expected_output, actual_output2)
        self.assertEqual(expected_output, actual_output3)

    def test_edit_account_as_supervisor(self):
        self.ui.current_user = self.tst_supervisor
        new_phone = '414-368-6425'
        expected_output = 'Account updated'
        actual_output1 = self.ui.edit_account(self.tst_ta.user, phone_number=new_phone)
        actual_output2 = self.ui.edit_account(self.tst_instructor.user, phone_number=new_phone)
        actual_output3 = self.ui.edit_account(self.tst_administrator.user, phone_number=new_phone)
        actual_output4 = self.ui.edit_account(self.tst_supervisor.user, phone_number=new_phone)
        self.assertEqual(expected_output, actual_output1)
        self.assertEqual(expected_output, actual_output2)
        self.assertEqual(expected_output, actual_output3)
        self.assertEqual(expected_output, actual_output4)

    def test_edit_account_missing_username_arg(self):
        self.ui.current_user = self.tst_supervisor
        new_phone = '414-368-6425'
        expected_output = 'Missing argument. Please enter a username of the account to be edited'
        actual_output1 = self.ui.edit_account(username='', phone_number=new_phone)
        actual_output2 = self.ui.edit_account(username=' ', phone_number=new_phone)
        self.assertEqual(expected_output, actual_output1)
        self.assertEqual(expected_output, actual_output2)

    def test_edit_account_username_not_exist(self):
        self.ui.current_user = self.tst_supervisor
        new_phone = '414-368-6425'
        expected_output = 'Failed to edit account. Username not found'
        actual_output = self.ui.edit_account(username='notExist', phone_number=new_phone)
        self.assertEqual(expected_output, actual_output)

    def test_database_entry_correct(self):
        self.ui.current_user = self.tst_supervisor
        self.tst_ta.street_address = '123 Cherry Street Milwaukee WI 53210'
        self.tst_ta.email_address = 'old@email.com'
        self.tst_ta.phone_number = '262-500-3000'
        self.tst_ta.save()
        new_street = '1100 N GinNJuice Ln Margaritaville WI 12345'
        new_email = 'new@email.com'
        new_phone = '414-368-6425'
        self.ui.edit_account(self.tst_ta.user,
                             street_address=new_street, email_address=new_email, phone_number=new_phone)
        self.tst_ta = Account.objects.get(user=self.tst_ta.user)
        self.assertEqual(self.tst_ta.street_address, new_street)
        self.assertEqual(self.tst_ta.email_address, new_email)
        self.assertEqual(self.tst_ta.phone_number, new_phone)




