from ta_app.commands_interface import CommandsInterface
import ta_app.wsgi
from website.models import Account, Course, Lab


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

    def edit_account(self, username='', password='', role='', street_address='', email_address='', phone_number=''):
        if self.current_user == Account():
            return 'Please login'

        # check that current user has correct permissions to edit account
        cur_user_role = self.get_current_user().role
        account_to_edit = self.get_account(username)
        if cur_user_role != 'Supervisor' and cur_user_role != 'Administrator':
            return 'Failed to edit account. Insufficient permissions'
        if cur_user_role == 'Administrator' and account_to_edit.role == 'Supervisor':
            return 'Failed to edit account. Insufficient permissions'

        if username.strip(' ') == '':
            return 'Missing argument. Please enter a username of the account to be edited'
        if account_to_edit.id is None:
            return 'Failed to edit account. Username not found'

        if password.strip(' ') != '':
            account_to_edit.password = password
        if role.strip(' ') != '':
            account_to_edit.role = role
        if street_address.strip(' ') != '':
            account_to_edit.street_address = street_address
        if email_address.strip(' ') != '':
            account_to_edit.email_address = email_address
        if phone_number.strip(' ') != '':
            account_to_edit.phone_number = phone_number
        account_to_edit.save()
        return 'Account updated'

    def create_course(self, name="", section="", days="", time="", labs=""):
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor" and cur_user_role != "Administrator":
            return "You do not have permissions to create courses"
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
                           end_time=times[1])
                o.save()
                for lab in ls:
                    Lab(course=o, section=lab).save()
            return "Course " + name + " has been added to the data base with lab sections " + labs

    # helper timing conflict
    def overlap(self, start1, end1, start2, end2):
        """Does the range (start1, end1) overlap with (start2, end2)?"""
        return end1 >= start2 and end2 >= start1

    # helper schedule conflict
    def schedule_verification(self, this_schedule, user_schedule):
        if user_schedule is not None:
            these_days = this_schedule.days_of_week.split("/")
            this_st = this_schedule.start_time.replace(":", "")
            this_et = this_schedule.end_time.replace(":", "")
            for c in user_schedule:
                those_days = c.days_of_week.split("/")
                for d in these_days:
                    for cd in those_days:
                        if cd == d:
                            those_st = c.start_time.replace(":", "")
                            those_et = c.end_time.replace(":", "")
                            return self.overlap(this_st, this_et, those_st, those_et)

    def edit_lab(self, course_name="", section="", days="", time=""):
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor" and cur_user_role != "Administrator":
            return "You do not have permissions to edit labs"
        if course_name == "" or section == "" or days == "" or time == "":
            return "Please input valid arguments for all fields to edit a lab"
        else:
            d = days.split("/")
            valid1 = True
            for day in d:
                if day not in ["M", "T", "W", "R", "F", "S", "U", "O"]:
                    valid1 = False

            times = time.split("-")
            stl = times[0].split(":")
            etl = times[1].split(":")

            co = Course.objects.get(name=course_name)
            if not Course.objects.filter(name=course_name).exists():
                return "Course " + course_name + " is not present in the data base"
            if not Lab.objects.filter(course=co, section=section).exists():
                return "Lab " + course_name + " - " + section + " is not present in the data base"
            if len(section) > 3 or not section.isnumeric():
                return "Section must be a three digit number"
            if not valid1:
                return "Days of week are noted as M, T, W, R, F, S, U, O"
            if len(times[0]) > 5 or int(stl[0]) > 23 or int(stl[1]) > 59:
                return "valid start time is 00:00 to 23:59"
            if len(times[1]) > 5 or int(etl[0]) > 23 or int(etl[1]) > 59:
                return "valid end time is 00:00 to 23:59"
            if stl[0] > etl[0] or (stl[0] == etl[0] and stl[1] > etl[1]):
                return "end time can not be earlier than start time"

            lo = Lab.objects.get(course=co, section=section)

            lo = Lab.objects.get(course=co, section=section)
            lo.days_of_week = days
            times = time
            times_split = times.split("-")
            lo.start_time = times_split[0]
            lo.end_time = times_split[1]

            these_days = lo.days_of_week.split("/")
            this_st = lo.start_time.replace(":", "")
            this_et = lo.end_time.replace(":", "")

            those_days = co.days_of_week.split("/")
            for d in these_days:
                for cd in those_days:
                    if cd == d:
                        those_st = co.start_time.replace(":", "")
                        those_et = co.end_time.replace(":", "")
                        if self.overlap(this_st, this_et, those_st, those_et):
                            return "This lab's timing conflicts with it's lecture time"

            lo.save()
            return "Lab " + course_name + " " + section + " has been updated"

    def assign_instructor(self, user="", course=""):
        if user == "" or course == "":
            return "Please input valid arguments for both fields to assign an instructor to a course"
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor":
            return "You do not have permissions to assign instructors to courses"
        if not Account.objects.filter(user=user).exists():
            return "This user is not present in the data base"
        if not Course.objects.filter(name=course).exists():
            return "This course is not present in the data base"
        else:
            this_course = Course.objects.get(name=course)
            account = Account.objects.get(user=user)
            instructors_courses = Course.objects.filter(instructor=account)
            if self.schedule_verification(this_course, instructors_courses):
                                    return "This course conflicts with the instructor's current schedule"
            this_course.instructor = account
            this_course.save()
            return user + " has been added to as " + course + "s instructor"

    def assign_ta_to_course(self, user="", course=""):
        if user == "" or course == "":
            return "Please input valid arguments for both fields to assign a ta to a course"
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor":
            return "You do not have permissions to assign TAs to courses"
        if not Account.objects.filter(user=user).exists():
            return "This user is not present in the data base"
        if not Course.objects.filter(name=course).exists():
            return "This course is not present in the data base"
        else:
            this_course = Course.objects.get(name=course)
            account = Account.objects.get(user=user)
            tas_courses = Course.objects.filter(tas=account)
            if self.schedule_verification(this_course, tas_courses):
                return "This course conflicts with the TA's current schedule"
            this_course.tas.add(account)
            this_course.save()
            return user + " has been added as a TA to " + course

    def assign_ta_to_lab(self, user="", course="", lab=""):
        if user == "" or course == "" or lab == "":
            return "Please input valid arguments for all fields to assign a TA to a lab section"
        cur_user_role = self.get_current_user().role
        if cur_user_role != "Supervisor" and cur_user_role != "Instructor":
            return "You do not have permissions to assign TAs to labs"
        if not Account.objects.filter(user=user).exists():
            return "This user is not present in the data base"
        if not Course.objects.filter(name=course).exists():
            return "This course is not present in the data base"
        this_course = Course.objects.get(name=course)
        if not Lab.objects.filter(course=this_course, section=lab).exists():
            return "Course " + course + " does not have lab section " + lab + " present in the data base"
        this_lab = Lab.objects.get(course=this_course, section=lab)
        account = Account.objects.get(user=user)
        if not this_course.tas.filter(user=account.user).exists():
            return "This user is not assigned as a TA to this course"
        if this_lab.days_of_week is None or this_lab.start_time is None or this_lab.end_time is None:
            return "This lab section does not have a specified schedule yet"
        else:
            tas_courses = Course.objects.filter(tas=account)
            tas_labs = Lab.objects.filter(ta=account)
            if self.schedule_verification(this_lab, tas_courses) or self.schedule_verification(this_lab, tas_labs):
                return "This lab conflicts with the TA's current schedule"
            this_lab.ta = account
            this_lab.save()
            return user + " has been assigned as the TA to " + course + " " + lab

    def view_course_assignments(self):
        return ''

    def view_ta_assignments(self):
        return ''

    def read_contact_info(self):
        if self.current_user == Account():
            return 'Please login!'
        return list(Account.objects.all())

    def edit_contact_info(self, username='', password='', street_address="", email_address="", phone_number=""):
        if self.current_user == Account() or self.current_user is None:
            return "Can not edit account. No current user"
            # check that current user has correct permissions to edit account
        cur_user_role = self.get_current_user().role
        account_to_edit = self.get_account(username)
        if cur_user_role == 'Administrator' and account_to_edit.role == 'Supervisor':
            return 'Insufficient permissions to edit account'
        account_to_edit.user = username
        account_to_edit.password = password
        if street_address != "":
            account_to_edit.street_address = street_address
        if email_address != "":
            account_to_edit.email_address = email_address
        if phone_number != "":
            account_to_edit.phone_number = phone_number
        account_to_edit.save()
        return "Account has been updated"

    def help(self):
        commands = '<ol>'
        for i in self.command_list.keys():
            commands += "<li>" + i + "</li>"
            commands += '\n'
        return commands + "</ol>"

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


