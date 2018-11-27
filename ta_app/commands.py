from ta_app.commands_interface import CommandsInterface
from ta_app.DB_interface import DBConnect


class Commands(CommandsInterface):

    def __init__(self):
        self.current_user = ''

    def logout(self):
        return ''

    def create_course(self, name, section, days, times, labs):
        return ''

    def create_account(self, user, password, role):
        return ''

    def delete_account(self, user, password, role):
        return ''

    def edit_account(self, user):
        return ''

    def assign_instructor(self, user, course):
        return ''

    def assign_ta_to_course(self, user, course):
        return ''

    def assign_ta_to_lab(self, user, course, lab):
        return ''

    def read_contact_info(self):
        return ''

    def edit_contact_info(self):
        return ''

    def view_course_assignments(self):
        return ''

    def view_ta_assignments(self):
        return ''

    def help(self):
        return ''

    def get_current_user(self):
        return ''

    def login(self, user, password):
        return ''

    command_list = [login, help]

    def call_command(self, command, command_list):
        return ''
