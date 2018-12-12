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

    def test_edit_account_insufficient_permissions(self):
        self.ui.login('usrSupervisor', 'password')
        newPhone = '414-368-6425'
        expected_output = 'Failed to edit account. Insufficient permissions'
        actual_output = self.ui.edit_account(self.tst_ta.user, phone_number=newPhone)
        self.assertNotEqual(expected_output, actual_output)

    def test_edit_account_address(self):
        self.ui.login('usrSupervisor', 'password')
        newAddress = '1026 Lake Dr Milwaukee WI'
        expected_output = 'Account information successfully changed'
        actual_output = self.ui.edit_account(self.tst_ta.user, street_address=newAddress)
        self.assertEqual(expected_output, actual_output)

    def test_edit_account_phone(self):
        self.ui.login('usrSupervisor', 'password')
        newPhone = '414-368-6425'
        expected_output = 'Account information successfully changed'
        actual_output = self.ui.edit_account(self.tst_ta.user, phone_number=newPhone)
        self.assertEqual(expected_output, actual_output)
