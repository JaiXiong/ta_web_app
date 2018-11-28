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

    def delete_account(self, username=''):
        if username == '':
            return 'Failed to delete account. Invalid or missing argument'

        account_to_delete = self.get_account(username)
        cur_user_role = self.get_current_user().role
        if cur_user_role != 'Supervisor' and cur_user_role != 'Administrator':
            return 'Failed to delete account. Insufficient permissions'
        if cur_user_role == 'Administrator' and account_to_delete.role == 'Supervisor':
            return 'Failed to delete account. Insufficient permissions'
        if account_to_delete.id is None:
            return 'Failed to delete account. User not found'
        if Course.objects.filter(instructor=account_to_delete).exists():
            return 'Failed to delete account. User is assigned to a course'

        account_to_delete.delete()
        return 'Successfully deleted account'

    def edit_account(self, username, password, role, street_address, email_address, phone_number):
        return ''

    def create_course(self, name="", section="", days="", time="", labs=""):
        if name == "" or section == "" or days == "" or time == "" or labs == "":
            return "Please input valid arguments for all fields to create a course"
        else:
            d = days.split("/")
            valid1 = True
            for day in d:
                if day not in ["M", "T", "W", "R", "F", "S", "U", "O"]:
                    valid1 = False

            times = time.split("-")
            stl = times[0].split(":")
            etl = times[1].split(":")

            valid2 = True
            ls = labs.split("/")
            for lab in ls:
                if len(lab) > 3 or not lab.isnumeric():
                    valid2 = False

            if Course.objects.filter(name=name).exists():
                return "Course " + name + " - " + section + " already exists in the data base"
            elif len(section) > 3 or not section.isnumeric():
                return "Section must be a three digit number"
            elif not valid1:
                return "Days of week are noted as M, T, W, R, F, S, U, O"
            elif len(times[0]) > 5 or int(stl[0]) > 23 or int(stl[1]) > 59:
                return "valid start time is 00:00 to 23:59"
            elif len(times[1]) > 5 or int(etl[0]) > 23 or int(etl[1]) > 59:
                return "valid end time is 00:00 to 23:59"
            elif stl[0] > etl[0] or (stl[0] == etl[0] and stl[1] > etl[1]):
                return "end time can not be earlier than start time"
            elif not valid2:
                return "Lab sections must be a three digit number"
            else:
                o = Course(name=name,
                           section=section,
                           days_of_week=days,
                           start_time=times[0],
                           end_time=times[1],
                           lab_sections=labs)
                o.save()
            return "Course " + name + " has been added to the data base."

    def assign_instructor(self, user="", course=""):
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor":
            return "You do not have permissions to assign instructors to courses"
        if user == "" or course == "":
            return "Please input valid arguments for both fields to create assign an instructor to a course"

        if not Account.objects.filter(user=user).exists():
            return "This user is not present in the data base"

        if not Course.objects.filter(name=course).exists():
            return "This course is not present in the data base"
        else:
            this_course = Course.objects.get(name=course)
            account = Account.objects.get(user=user)
            instructors_courses = Course.objects.filter(instructor=account)
            if instructors_courses is not None:
                these_days = this_course.days_of_week.split("/")
                this_st = this_course.start_time.replace(":", "")
                this_et = this_course.end_time.replace(":", "")
                for c in instructors_courses:
                    those_days = c.days_of_week.split("/")
                    for d in these_days:
                        for cd in those_days:
                            if cd == d:
                                those_st = c.start_time.replace(":", "")
                                those_et = c.end_time.replace(":", "")

                                if self.overlap(this_st, this_et, those_st, those_et):
                                    return "This course conflicts with the instructor's current schedule"
            this_course.instructor = account
            this_course.save()
            return user + " has been added as " + course + "'s instructor"

    def assign_ta_to_course(self, user="", course=""):
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor":
            return "You do not have permissions to assign TAs to courses"
        if user == "" or course == "":
            return "Please input valid arguments for both fields to create assign an instructor to a course"
        if not Account.objects.filter(user=user).exists():
            return "This user is not present in the data base"
        if not Course.objects.filter(name=course).exists():
            return "This course is not present in the data base"
        else:
            this_course = Course.objects.get(name=course)
            account = Account.objects.get(user=user)
            tas_courses = Course.objects.filter(tas=account)
            if tas_courses is not None:
                these_days = this_course.days_of_week.split("/")
                this_st = this_course.start_time.replace(":", "")
                this_et = this_course.end_time.replace(":", "")
                for c in tas_courses:
                    those_days = c.days_of_week.split("/")
                    for d in these_days:
                        for cd in those_days:
                            if cd == d:
                                those_st = c.start_time.replace(":", "")
                                those_et = c.end_time.replace(":", "")
                                if self.overlap(this_st, this_et, those_st, those_et):
                                    return "This course conflicts with the TA's current schedule"
            this_course.tas.add(account)
            this_course.save()
            return user + " has been added as a TA to " + course

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
        commands = '<ol>'
        for i in self.command_list.keys():
            commands += '<li><b>' + i + '</b>'
            if i == 'login':
                commands += '&nbsp &ltusername&gt &nbsp&ltpassword&gt'
            elif i == 'create_account':
                commands += '&nbsp &ltusername&gt &nbsp&ltpassword&gt &nbsp&ltrole&gt'
            elif i == 'delete_account':
                commands += '&nbsp &ltusername&gt'
            elif i == 'create_course':
                commands += ' &nbsp&ltname&gt &nbsp&ltsection&gt &nbsp&ltdays&gt &nbsp&lttimes&gt &nbsp&ltlabs&gt'
            elif i == 'assign_instructor':
                commands += ' &nbsp&ltusername&gt &nbsp&ltcourse&gt'
            elif i == 'assign_ta_to_course':
                commands += ' &nbsp&ltusername&gt &nbsp&ltcourse&gt'
            elif i == 'assign_ta_to_lab':
                commands += ' &nbsp&ltusername&gt &nbsp&ltcourse&gt &nbsp&ltlab&gt'
            elif i == 'edit_account':
                commands += ' &nbsp&ltusername&gt &nbsp&ltpassword&gt &nbsp&ltrole&gt ' \
                            '&nbsp&ltstreet_address&gt &nbsp&ltemail&gt &nbsp&ltphone&gt'
            commands += '</li>\n'
        return commands + '</ol>'

    def call_command(self, user_input=''):
        if user_input == '':
            return ''
        try:
            params = user_input.split()
            call = params[0]
            args = params[1:len(params)]
            return self.command_list.get(call, lambda *_: "ERROR: this is not an available command")(*args)
        except TypeError:
            return 'Too many arguments entered. Try again!'

    def get_current_user(self):
        return self.current_user

    def get_account(self, username=''):
        accounts = list(Account.objects.filter(user=username))
        if len(accounts) == 1:
            return accounts.__getitem__(0)
        return Account()

    def overlap(self, start1, end1, start2, end2):
        """Does the range (start1, end1) overlap with (start2, end2)?"""
        return end1 >= start2 and end2 >= start1

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


