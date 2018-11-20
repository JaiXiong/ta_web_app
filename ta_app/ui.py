from ta_app.db_connect_object import DBConnection
from ta_app.account_object import Account
from ta_app.course_object import Course
from ta_app.superuser_login import Superuser


class UI:

    sCurrentUser = ""

    def __init__(self):
        self.sCurrentUser = ""
        self.accountsDB = self.connect_db('C:/Users/user/PycharmProjects/ta_app/DB_Files/accounts.csv')
        self.coursesDB = self.connect_db('C:/Users/user/PycharmProjects/ta_app/DB_Files/courses.csv')
        self.uiCommandSwitcher = {
            "help": lambda *_: self.help(),
            "login": lambda *_: self.login(*_),
            "logout": lambda: self.logout(),
            "create_course": lambda *_: self.create_course(*_),
            "create_account": lambda *_: self.create_account(*_),
            "delete_account": lambda *_: self.delete_account(*_),
            "edit_account": lambda *_: self.edit_account(*_),
            "assign_instructor": lambda *_: self.assign_instructor(*_),
            "assign_ta_to_course": lambda *_: self.assign_ta_to_course(*_),
            "assign_ta_to_lab": lambda *_: self.assign_ta_to_lab(*_),
            "edit_contact_info": lambda *_: self.edit_contact_info(),
            "view_course_assignments": lambda *_: self.view_course_assignments(),
            "view_ta_assignments": lambda *_: self.view_ta_assignments(),
            "read_contact_info": lambda *_: self.read_contact_info()
        }

    def command(self, pscommand):
        paramslist = pscommand.split()
        call = paramslist[0]
        args = paramslist[1:len(paramslist)]
        return self.uiCommandSwitcher.get(call, lambda *_: "ERROR: this is not an available command")(*args)

    def connect_db(self, dbPath=''):
        db_connection = DBConnection()
        try:
            db_connection.connect(dbPath)
        except OSError or ValueError:
            print('failed to connect to db ' + dbPath)
        return db_connection

    def disconnect_db(self):
        return True

    def help(self):
        return "help string"

    def login(self, psuser="", pspassword=""):
        super = Superuser()
        if super.superuser_authentication(psuser, pspassword) is True:
            self.set_user(psuser)
            return 'login successful...'
        else:
            return 'login failed! bad username/ password'

    def logout(self):
        if self.sCurrentUser == '':
            return "no current user..."
        else:
            self.sCurrentUser = ''
            return 'logout successful...'

    def create_course(self, psname="", pssection="", psdaysofweek="", pstimes="", pslabsection=""):
        if psname == "" or pssection == "" or psdaysofweek == "" or pstimes == "":
            raise ValueError("Please fill in all required fields to create a course")
        else:
            days = psdaysofweek.split("/")
            labs = pslabsection.split("/")
            times = pstimes.split("-")
            co = Course(psname, pssection, days, times[0], times[1], labs)
            self.coursesDB.add_course(co)

    def create_account(self, psuser="", pspassword="", psrole=""):
        if self.get_current_user() != 'default_superuser':
            return 'Failed to create account. Insufficient permissions'
        if psuser == "" or pspassword == "" or psrole == "":
            return 'Failed to create account. Invalid or missing argument'
        new_account = Account(psuser, pspassword, psrole)
        self.accountsDB.add_account(new_account)
        return 'Successfully created account'

    def delete_account(self, psuser="", pspassword="", psrole=""):
        if self.get_current_user() != 'default_superuser':
            return 'Failed to delete account. Insufficient permissions'
        if psuser == '':
            return 'Failed to delete account. Invalid or missing argument'
        ac = Account(psuser, pspassword, psrole)
        result = self.accountsDB.remove_account(ac)
        if not result:
            return "Failed to delete account. User not found"
        return "Successfully deleted account"

    def edit_account(self, psuser=""):
        return ""

    def assign_instructor(self, psuser="", pscourse=""):
        return ""

    def assign_ta_to_course(self, psuser="", pscourse=""):
        return ""

    def assign_ta_to_lab(self, psuser="", pscourse="", pslabsection=""):
        return ""

    def edit_contact_info(self):
        return ""

    def view_course_assignments(self):
        return ""

    def view_ta_assignments(self):
        return ""

    def read_contact_info(self):
        return ""

    def set_user(self, u):
        if u:
            self.sCurrentUser = u
        else:
            raise ValueError("User cannot be blank")

    def get_current_user(self):
        return self.sCurrentUser
