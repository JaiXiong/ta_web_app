from django.test import TestCase
from ta_app.commands import Commands
from website.models import Account


class TestEditContactInfo(TestCase):

    def setUp(self):
        Account.objects.all().delete()
        self.ui = Commands()
        self.tst_supervisor = Account(user='usrSupervisor', password='password', role='Supervisor', street_address="123 Supervisor Drive", email_address="supervisor@school.org", phone_number="000-111-2222")
        self.tst_administrator = Account(user='usrAdministrator', password='password', role='Administrator', street_address="123 Administrator Drive", email_address="administrator@school.org", phone_number="111-222-3333")
        self.tst_instructor = Account(user='usrInstructor', password='password', role='Instructor', street_address="123 Instructor Drive", email_address="instructor@school.org", phone_number="222-333-4444")
        self.tst_ta = Account(user='usrTA', password='password', role='TA')
        self.tst_supervisor.save()
        self.tst_administrator.save()
        self.tst_instructor.save()
        self.tst_ta.save()

    def test_edit_contact_info_no_user_inDB(self):
        Account.objects.filter(user="usrTA").all().delete()
        expected_output = "No users with that username"
        self.ui.login(self.tst_instructor.user, self.tst_instructor.password)
        new_addr = "1333 New Drive"
        actual_output = self.ui.edit_contact_info(username=self.tst_ta.user, street_address=new_addr)
        self.assertEqual(expected_output, actual_output)

    def test_edit_contact_info_no_user_no_data(self):
        self.ui.current_user = None
        expected_output = "Can not edit account. No current user"
        actual_output = self.ui.edit_contact_info()
        self.assertEqual(expected_output, actual_output)

    def test_edit_contact_info_no_user_data(self):
        self.ui.current_user = None
        expected_output = "Can not edit account. No current user"
        actual_output = self.ui.edit_contact_info(username='usrInstructor', password='password', street_address="123 Instructor Drive", email_address="instructor@school.org", phone_number="222-333-4444")
        self.assertEqual(expected_output, actual_output)

    def test_edit_contact_info_user_insufficient_permissions(self):
        self.ui.login(self.tst_ta.user, self.tst_ta.password)
        expected_output = "Insufficient permissions to edit account"
        actual_output = self.ui.edit_contact_info(username=self.tst_ta.user, password=self.tst_ta.password, street_address="invalid")
        self.assertEqual(expected_output, actual_output)

    def test_edit_contact_info_user_instructor_no_data(self):
        self.ui.login(self.tst_instructor.user, self.tst_instructor.password)
        actual_output = self.ui.edit_contact_info(username=self.tst_instructor.user, password=self.tst_administrator.password)
        self.assertEqual(self.tst_instructor.user, actual_output.user)
        self.assertEqual(self.tst_instructor.password, actual_output.password)
        self.assertEqual(self.tst_instructor.role, actual_output.role)
        self.assertEqual(self.tst_instructor.street_address, actual_output.street_address)
        self.assertEqual(self.tst_instructor.email_address, actual_output.email_address)
        self.assertEqual(self.tst_instructor.phone_number, actual_output.phone_number)

    def test_edit_contact_info_user_administrator_no_data(self):
        self.ui.login(self.tst_administrator.user, self.tst_administrator.password)
        actual_output = self.ui.edit_contact_info(username=self.tst_administrator.user, password=self.tst_administrator.password)
        self.assertEqual(self.tst_administrator.user, actual_output.user)
        self.assertEqual(self.tst_administrator.password, actual_output.password)
        self.assertEqual(self.tst_administrator.role, actual_output.role)
        self.assertEqual(self.tst_administrator.street_address, actual_output.street_address)
        self.assertEqual(self.tst_administrator.email_address, actual_output.email_address)
        self.assertEqual(self.tst_administrator.phone_number, actual_output.phone_number)

    def test_edit_account_info_street_address(self):
        self.ui.login(self.tst_instructor.user, self.tst_instructor.password)
        new_addr = "1333 New Drive"
        actual_output = self.ui.edit_contact_info(username=self.tst_instructor.user, password=self.tst_instructor.password, street_address=new_addr)
        self.assertEqual(self.tst_instructor.user, actual_output.user)
        self.assertEqual(self.tst_instructor.password, actual_output.password)
        self.assertEqual(self.tst_instructor.role, actual_output.role)
        self.assertEqual(new_addr, actual_output.street_address)
        self.assertEqual(self.tst_instructor.email_address, actual_output.email_address)
        self.assertEqual(self.tst_instructor.phone_number, actual_output.phone_number)

    def test_edit_account_info_email(self):
        self.ui.login(self.tst_instructor.user, self.tst_instructor.password)
        new_email = "new@email.com"
        actual_output = self.ui.edit_contact_info(username=self.tst_instructor.user, password=self.tst_instructor.password, email_address=new_email)
        self.assertEqual(self.tst_instructor.user, actual_output.user)
        self.assertEqual(self.tst_instructor.password, actual_output.password)
        self.assertEqual(self.tst_instructor.role, actual_output.role)
        self.assertEqual(self.tst_instructor.street_address, actual_output.street_address)
        self.assertEqual(new_email, actual_output.email_address)
        self.assertEqual(self.tst_instructor.phone_number, actual_output.phone_number)

    def test_edit_account_phone_number(self):
        self.ui.login(self.tst_instructor.user, self.tst_instructor.password)
        new_phone = "111-111-1111"
        actual_output = self.ui.edit_contact_info(username=self.tst_instructor.user, password=self.tst_instructor.password, phone_number=new_phone)
        self.assertEqual(self.tst_instructor.user, actual_output.user)
        self.assertEqual(self.tst_instructor.password, actual_output.password)
        self.assertEqual(self.tst_instructor.role, actual_output.role)
        self.assertEqual(self.tst_instructor.street_address, actual_output.street_address)
        self.assertEqual(self.tst_instructor.email_address, actual_output.email_address)
        self.assertEqual(new_phone, actual_output.phone_number)

    def test_edit_account_multiple(self):
        self.ui.login(self.tst_instructor.user, self.tst_instructor.password)
        new_addr = "1333 New Drive"
        new_phone = "111-111-1111"
        actual_output = self.ui.edit_contact_info(username=self.tst_instructor.user, password=self.tst_instructor.password, street_address=new_addr, phone_number=new_phone)
        self.assertEqual(self.tst_instructor.user, actual_output.user)
        self.assertEqual(self.tst_instructor.password, actual_output.password)
        self.assertEqual(self.tst_instructor.role, actual_output.role)
        self.assertEqual(new_addr, actual_output.street_address)
        self.assertEqual(self.tst_instructor.email_address, actual_output.email_address)
        self.assertEqual(new_phone, actual_output.phone_number)

















