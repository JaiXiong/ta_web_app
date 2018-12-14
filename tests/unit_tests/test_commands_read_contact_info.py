from django.test import TestCase
from ta_app.commands import Commands
import ta_app.wsgi
from website.models import Account


class TestReadContactInfo(TestCase):

    def setUp(self):
        self.ui = Commands()
        self.tst_supervisor = Account(user='usrSupervisor', password='password', role='Supervisor',
                                      street_address='3200 N Newport Ave Milwaukee WI 53211',
                                      email_address='supervisor@uwm.edu',
                                      phone_number='414-736-9565')
        self.tst_administrator = Account(user='usrAdministrator', password='password', role='Administrator',
                                         street_address='1026 S 27th St Milwaukee WI 53221',
                                         email_address='administrator@uwm.edu',
                                         phone_number='920-223-5166')
        self.tst_instructor = Account(user='usrInstructor', password='password', role='Instructor',
                                      street_address='2466 N 13th St Milwaukee WI 53201',
                                      email_address='instructor@uwm.edu',
                                      phone_number='262-115-1107')
        self.tst_ta = Account(user='usrTA', password='password', role='TA',
                              street_address='2466A N 13th St Milwaukee WI 53201',
                              email_address='ta@uwm.edu',
                              phone_number='262-115-1109')
        self.tst_supervisor.save()
        self.tst_administrator.save()
        self.tst_instructor.save()
        self.tst_ta.save()

        self.expected_output = list(Account.objects.all())

    def test_supervisor_read_contact_info(self):
        self.ui.current_user = self.tst_supervisor
        actual_output = self.ui.read_contact_info()
        self.assertEqual(actual_output, self.expected_output)

    def test_administrator_read_contact_info(self):
        self.ui.current_user = self.tst_administrator
        actual_output = self.ui.read_contact_info()
        self.assertEqual(actual_output, self.expected_output)

    def test_instructor_read_contact_info(self):
        self.ui.current_user = self.tst_instructor
        actual_output = self.ui.read_contact_info()
        self.assertEqual(actual_output, self.expected_output)

    def test_ta_read_contact_info(self):
        self.ui.current_user = self.tst_ta
        actual_output = self.ui.read_contact_info()
        self.assertEqual(actual_output, self.expected_output)
