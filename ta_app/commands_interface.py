import abc


class CommandsInterface(abc.ABC):

    @abc.abstractmethod
    def login(self, username, password):
        return ''

    @abc.abstractmethod
    def logout(self):
        return ''

    @abc.abstractmethod
    def create_account(self, username, password, role):
        return ''

    @abc.abstractmethod
    def delete_account(self, username):
        return ''

    @abc.abstractmethod
    def edit_account(self, username, password, role, street_address, email_address, phone_number):
        return ''

    @abc.abstractmethod
    def create_course(self, name, section, days, times, labs):
        return ''

    @abc.abstractmethod
    def assign_instructor(self, username, course):
        return ''

    @abc.abstractmethod
    def assign_ta_to_course(self, username, course):
        return ''

    @abc.abstractmethod
    def assign_ta_to_lab(self, username, course, lab):
        return ''

    @abc.abstractmethod
    def view_course_assignments(self):
        return ''

    @abc.abstractmethod
    def view_ta_assignments(self):
        return ''

    @abc.abstractmethod
    def read_contact_info(self):
        return ''

    @abc.abstractmethod
    def edit_contact_info(self, street_address, email_address, phone_number):
        return ''

    @abc.abstractmethod
    def help(self):
        return ''

    @abc.abstractmethod
    def call_command(self, user_input):
        return ''

    @abc.abstractmethod
    def get_current_user(self):
        return ''
