from ta_app.commands_interface import CommandsInterface
import ta_app.wsgi
from website.models import Account, Course


class Commands(CommandsInterface):
    def __init__(self):
        self.current_user = Account()
        self.command_list = {
            "login": lambda *_: self.login(*_),
            "help": lambda: self.help()
        }

    def login(self, username='', password=''):
        if username == '' or password == '':
            return 'login failed! bad username/ password'

        existing_account = self.get_account(username)
        if existing_account.user == username and existing_account.password == password:
            self.current_user = existing_account
            self.set_command_list()
            return 'login successful...'
        return 'login failed! bad username/ password'

    def logout(self):
        self.current_user = Account()
        self.set_command_list()
        return 'logout successful...'

    def create_account(self, username='', password='', role=''):
        if username == '' or password == '' or role == '':
            return 'Failed to create account. Invalid or missing argument'

        # check that current user has correct permissions to create account
        cur_user_role = self.get_current_user().role
        if cur_user_role != 'Supervisor' and cur_user_role != 'Administrator':
            return 'Failed to create account. Insufficient permissions'
        if cur_user_role == 'Administrator' and role == 'Supervisor':
            return 'Failed to create account. Insufficient permissions'

        valid_roles = ['Supervisor', 'Administrator', 'Instructor', 'TA']
        role_is_valid = valid_roles.__contains__(role)
        if not role_is_valid:
            msg = 'Failed to create account. Invalid account type'
            msg += '\nValid roles are ' + str(valid_roles)
            return msg

        existing_account = self.get_account(username)
        if existing_account.id is not None:
            return 'Failed to create account. User already exists'

        new_account = Account(user=username, password=password, role=role)
        new_account.save()
        return 'Successfully created account'

    def delete_account(self, user, password, role):
        return ''

    def edit_account(self, user):
        return ''

    def create_course(self, name, section, days, times, labs):
        return ''

    def assign_instructor(self, user, course):
        return ''

    def assign_ta_to_course(self, user, course):
        return ''

    def assign_ta_to_lab(self, user, course, lab):
        return ''

    def view_course_assignments(self):
        if self.current_user.user == "":
            return "Failed to view course assignments. No current user"
        if self.current_user.role == "TA":
            return 'Failed to view course assignments. Insufficient permissions'
        output = ""
        course_list = list(Course.objects.all())
        for course in course_list:
            if course.instructor is not None:
                output += "<p>Course: " + course.name + ", Instructor: " + course.instructor.user + "</p><br />"
        return output

    def view_ta_assignments(self):
        if self.current_user.user == "":
            return "Failed to view ta assignments. No current user"
        output = ""
        course_list = list(Course.objects.all())
        for course in course_list:
            if course.instructor is not None and course.tas is not None:
                ta_list = list(course.tas.all())
                ta_str = ""
                for ta in ta_list:
                    ta_str += ta.user + " "
                output += "<p>Course: " + course.name + ", Section: " + course.section + ", TA(s): " + ta_str + "</p><br />"
        return output

    def read_contact_info(self):
        return ''

    def edit_contact_info(self):
        return ''

    def help(self):
        commands = ''
        for i in self.command_list.keys():
            commands += i
            commands += '\n'
        return commands

    def call_command(self, user_input):
        params = user_input.split()
        call = params[0]
        args = params[1:len(params)]
        return self.command_list.get(call, lambda *_: "ERROR: this is not an available command")(*args)

    def get_current_user(self):
        return self.current_user

    def get_account(self, username=''):
        accounts = list(Account.objects.filter(user=username))
        if len(accounts) == 1:
            return accounts.__getitem__(0)
        return Account()

    def set_command_list(self):
        if self.current_user.id is None:
            self.command_list = {
                "login": lambda *_: self.login(*_),
                "help": lambda: self.help()
            }
        role = self.current_user.role
        if role == 'Supervisor':
            self.command_list = {
                "logout": lambda: self.logout(),
                "create_account": lambda *_: self.create_account(*_),
                "delete_account": lambda *_: self.delete_account(*_),
                "edit_account": lambda *_: self.edit_account(*_),
                "create_course": lambda *_: self.create_course(*_),
                "assign_instructor": lambda *_: self.assign_instructor(*_),
                "assign_ta_to_course": lambda *_: self.assign_ta_to_course(*_),
                "assign_ta_to_lab": lambda *_: self.assign_ta_to_lab(*_),
                "view_course_assignments": lambda *_: self.view_course_assignments(),
                "view_ta_assignments": lambda *_: self.view_ta_assignments(),
                "edit_contact_info": lambda *_: self.edit_contact_info(),
                "read_contact_info": lambda *_: self.read_contact_info(),
                "help": lambda *_: self.help()
            }
        if role == 'Administrator':
            self.command_list = {
                "logout": lambda: self.logout(),
                "create_account": lambda *_: self.create_account(*_),
                "delete_account": lambda *_: self.delete_account(*_),
                "edit_account": lambda *_: self.edit_account(*_),
                "create_course": lambda *_: self.create_course(*_),
                "view_course_assignments": lambda *_: self.view_course_assignments(),
                "view_ta_assignments": lambda *_: self.view_ta_assignments(),
                "edit_contact_info": lambda *_: self.edit_contact_info(),
                "read_contact_info": lambda *_: self.read_contact_info(),
                "help": lambda *_: self.help()
            }
        if role == 'Instructor':
            self.command_list = {
                "logout": lambda: self.logout(),
                "assign_ta_to_lab": lambda *_: self.assign_ta_to_lab(*_),
                "view_course_assignments": lambda *_: self.view_course_assignments(),
                "view_ta_assignments": lambda *_: self.view_ta_assignments(),
                "edit_contact_info": lambda *_: self.edit_contact_info(),
                "read_contact_info": lambda *_: self.read_contact_info(),
                "help": lambda *_: self.help()
            }
        if role == 'TA':
            self.command_list = {
                "logout": lambda: self.logout(),
                "view_ta_assignments": lambda *_: self.view_ta_assignments(),
                "edit_contact_info": lambda *_: self.edit_contact_info(),
                "read_contact_info": lambda *_: self.read_contact_info(),
                "help": lambda *_: self.help()
            }


