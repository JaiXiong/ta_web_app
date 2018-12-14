from django.test import TestCase
from ta_app.commands import Commands
import ta_app.wsgi
from website.models import Account, Course


class TestCommands(TestCase):

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

        self.tst_course = Course(name="EE-554", section="004", days_of_week="M/W/F",
                                 start_time="11:00", end_time="11:50")
        self.tst_course.save()

    def test_call_command_valid(self):
        self.ui.current_user = Account()
        self.ui.set_command_list()
        output1 = self.ui.call_command('help')
        output2 = self.ui.call_command('login usrSupervisor password')
        output3 = self.ui.call_command('logout')
        self.assertNotEqual(output1, 'You should type something...')
        self.assertNotEqual(output2, 'You should type something...')
        self.assertNotEqual(output3, 'You should type something...')
        self.assertNotEqual(output1, 'Too many arguments entered. Try again!')
        self.assertNotEqual(output2, 'Too many arguments entered. Try again!')
        self.assertNotEqual(output3, 'Too many arguments entered. Try again!')
        self.assertNotEqual(output1, 'ERROR: this is not an available command')
        self.assertNotEqual(output2, 'ERROR: this is not an available command')
        self.assertNotEqual(output3, 'ERROR: this is not an available command')

    def testCallCommandInvalid(self):
        expected_output = 'ERROR: this is not an available command'
        actual_output = self.ui.call_command('invalidCommand')
        self.assertEqual(expected_output, actual_output)

    def test_call_command_too_many_args(self):
        expected_output = 'Too many arguments entered. Try again!'
        actual_output = self.ui.call_command('login user password oops')
        self.assertEqual(expected_output, actual_output)

    def test_call_command_no_args(self):
        expected_output = ''
        actual_output = self.ui.call_command()
        self.assertEqual(expected_output, actual_output)

    def test_help_with_no_current_user(self):
        self.ui.current_user = Account()
        output = self.ui.help()
        self.assertTrue(output.find('login'))
        self.assertTrue(output.find('help'))

    def test_help_as_supervisor(self):
        self.ui.current_user = self.tst_supervisor
        output = self.ui.help()
        self.assertTrue(output.find('logout'))
        self.assertTrue(output.find('create_account'))
        self.assertTrue(output.find('delete_account'))
        self.assertTrue(output.find('edit_account'))
        self.assertTrue(output.find('create_account'))
        self.assertTrue(output.find('assign_instructor'))
        self.assertTrue(output.find('assign_ta_to_course'))
        self.assertTrue(output.find('assign_ta_to_lab'))
        self.assertTrue(output.find('view_course_assignments'))
        self.assertTrue(output.find('view_ta_assignments'))
        self.assertTrue(output.find('edit_contact_info'))
        self.assertTrue(output.find('read_contact_info'))
        self.assertTrue(output.find('help'))

    def test_help_as_administrator(self):
        self.ui.current_user = self.tst_administrator
        output = self.ui.help()
        self.assertTrue(output.find('logout'))
        self.assertTrue(output.find('create_account'))
        self.assertTrue(output.find('delete_account'))
        self.assertTrue(output.find('edit_account'))
        self.assertTrue(output.find('create_account'))
        self.assertTrue(output.find('view_course_assignments'))
        self.assertTrue(output.find('view_ta_assignments'))
        self.assertTrue(output.find('edit_contact_info'))
        self.assertTrue(output.find('read_contact_info'))
        self.assertTrue(output.find('help'))

    def test_help_as_instructor(self):
        self.ui.current_user = self.tst_instructor
        output = self.ui.help()
        self.assertTrue(output.find('logout'))
        self.assertTrue(output.find('assign_ta_to_lab'))
        self.assertTrue(output.find('view_course_assignments'))
        self.assertTrue(output.find('view_ta_assignments'))
        self.assertTrue(output.find('edit_contact_info'))
        self.assertTrue(output.find('read_contact_info'))
        self.assertTrue(output.find('help'))

    def test_help_as_ta(self):
        self.ui.current_user = self.tst_ta
        output = self.ui.help()
        self.assertTrue(output.find('logout'))
        self.assertTrue(output.find('view_ta_assignments'))
        self.assertTrue(output.find('edit_contact_info'))
        self.assertTrue(output.find('read_contact_info'))
        self.assertTrue(output.find('help'))

    def test_login_bad_username(self):
        self.ui.current_user = Account()
        username = 'badUsername'
        expected_output = 'login failed! bad username/ password'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertNotEqual(self.ui.current_user.user, username)
        self.assertTrue(self.ui.current_user.id is None)

    def test_login_bad_password(self):
        self.ui.current_user = Account()
        username = 'usrSupervisor'
        expected_output = 'login failed! bad username/ password'
        actual_output = self.ui.login(username, 'badPassword')
        self.assertEqual(expected_output, actual_output)
        self.assertNotEqual(self.ui.current_user.user, username)
        self.assertTrue(self.ui.current_user.id is None)

    def test_login_supervisor(self):
        self.ui.current_user = Account()
        username = 'usrSupervisor'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_supervisor)

        commands = self.ui.command_list
        expected_num_commands = 13
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('delete_account'))
        self.assertTrue(commands.__contains__('edit_account'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('assign_instructor'))
        self.assertTrue(commands.__contains__('assign_ta_to_course'))
        self.assertTrue(commands.__contains__('assign_ta_to_lab'))
        self.assertTrue(commands.__contains__('view_course_assignments'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_login_administrator(self):
        self.ui.current_user = Account()
        username = 'usrAdministrator'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_administrator)

        commands = self.ui.command_list
        expected_num_commands = 10
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('delete_account'))
        self.assertTrue(commands.__contains__('edit_account'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('view_course_assignments'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_login_instructor(self):
        self.ui.current_user = Account()
        username = 'usrInstructor'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_instructor)

        commands = self.ui.command_list
        expected_num_commands = 7
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('assign_ta_to_lab'))
        self.assertTrue(commands.__contains__('view_course_assignments'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_login_ta(self):
        self.ui.current_user = Account()
        username = 'usrTA'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_ta)

        commands = self.ui.command_list
        expected_num_commands = 5
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_logout(self):
        self.ui.login('usrSupervisor', 'password')
        expected_output = 'logout successful...'
        actual_output = self.ui.logout()
        self.assertEqual(expected_output, actual_output)
        self.assertIsNone(self.ui.get_current_user().id)

        commands = self.ui.command_list
        expected_num_commands = 2
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('login'))
        self.assertTrue(commands.__contains__('help'))

    def test_create_account_as_supervisor(self):
        self.ui.login('usrSupervisor', 'password')
        username = 'tstCreatSupervisor'
        password = 'password'
        role = 'Supervisor'
        expected_output = 'Successfully created account'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.assertIsNotNone(created_account.id)
        self.assertEqual(created_account.user, username)
        self.assertEqual(created_account.password, password)
        self.assertEqual(created_account.role, role)

    def test_create_account_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        username = 'tstCreatSupervisor'
        password = 'password'
        role = 'TA'
        expected_output = 'Successfully created account'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.assertIsNotNone(created_account.id)
        self.assertEqual(created_account.user, username)
        self.assertEqual(created_account.password, password)
        self.assertEqual(created_account.role, role)

    def test_create_supervisor_account_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        username = 'tstCreatSupervisorAsAdmin'
        password = 'password'
        role = 'Supervisor'
        expected_output = 'Failed to create account. Insufficient permissions'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.assertIsNone(created_account.id)

    def test_create_account_as_instructor(self):
        self.ui.login('usrInstructor', 'password')
        username = 'tstCreatTA'
        password = 'password'
        role = 'TA'
        expected_output = 'Failed to create account. Insufficient permissions'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.assertIsNone(created_account.id)

    def test_create_account_as_ta(self):
        self.ui.login('usrTA', 'password')
        username = 'tstCreatTA'
        password = 'password'
        role = 'TA'
        initial_count = Account.objects.count()
        expected_output = 'Failed to create account. Insufficient permissions'
        actual_output = self.ui.create_account(username, password, role)
        final_count = Account.objects.count()
        created_account = self.ui.get_account(username)
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)
        self.assertIsNone(created_account.id)

    def test_create_account_existing_user(self):
        self.ui.login('usrSupervisor', 'password')
        username = 'usrTA'
        password = 'password'
        role = 'TA'
        expected_output = 'Failed to create account. User already exists'
        initial_count = Account.objects.count()
        actual_output = self.ui.create_account(username, password, role)
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)

    def test_delete_account_as_supervisor(self):
        self.ui.login('usrSupervisor', 'password')
        self.ui.create_account('tstDeleteAcc', 'password', 'TA')
        expected_output = 'Successfully deleted account'
        initial_count = Account.objects.count()
        expected_count = initial_count - 1
        actual_output = self.ui.delete_account('tstDeleteAcc')
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_count, final_count)

    def test_delete_account_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        self.ui.create_account('tstDeleteAcc', 'password', 'TA')
        initial_count = Account.objects.count()
        expected_count = initial_count - 1
        expected_output = 'Successfully deleted account'
        actual_output = self.ui.delete_account('tstDeleteAcc')
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_count, final_count)

    def test_delete_account_not_exist(self):
        self.ui.login('usrSupervisor', 'password')
        expected_output = 'Failed to delete account. User not found'
        initial_count = Account.objects.count()
        actual_output = self.ui.delete_account('notExist')
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)

    def test_delete_supervisor_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        expected_output = 'Failed to delete account. Insufficient permissions'
        initial_count = Account.objects.count()
        actual_output = self.ui.delete_account('usrSupervisor')
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)

    def test_delete_account_as_Instructor(self):
        self.ui.login('usrInstructor', 'password')
        expected_output = 'Failed to delete account. Insufficient permissions'
        initial_count = Account.objects.count()
        actual_output = self.ui.delete_account('usrTA')
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)

    def test_delete_account_as_TA(self):
        self.ui.login('usrTA', 'password')
        expected_output = 'Failed to delete account. Insufficient permissions'
        initial_count = Account.objects.count()
        actual_output = self.ui.delete_account('usrTA')
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)

    def test_delete_account_assigned_to_course(self):
        self.ui.login('usrSupervisor', 'password')
        self.tst_course.instructor = self.tst_instructor
        self.tst_course.save()
        self.assertEqual(self.tst_course.instructor, self.tst_instructor)
        num_courses_initial = Course.objects.count()
        num_accounts_initial = Account.objects.count()
        expected_output = 'Failed to delete account. User is assigned to a course'
        actual_output = self.ui.delete_account(self.tst_instructor.user)
        self.assertEqual(self.tst_course.instructor, self.tst_instructor)
        num_courses_final = Course.objects.count()
        num_accounts_final = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(num_accounts_initial, num_accounts_final)
        self.assertEqual(num_courses_initial, num_courses_final)

