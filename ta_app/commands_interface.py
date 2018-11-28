import abc


class CommandsInterface(abc.ABC):

    @abc.abstractmethod
    def login(self, username, password):
        return ''

    @abc.abstractmethod
    def logout(self):
        return ''

    @abc.abstractmethod
    def create_account(self, user, password, role):
        return ''

    @abc.abstractmethod
    def delete_account(self, user):
        return ''

    @abc.abstractmethod
    def edit_account(self, user):
        return ''

    @abc.abstractmethod
    def create_course(self, name, section, days, times, labs):
        return ''

    @abc.abstractmethod
    def assign_instructor(self, user, course):
        return ''

    @abc.abstractmethod
    def assign_ta_to_course(self, user, course):
        return ''

    @abc.abstractmethod
    def assign_ta_to_lab(self, user, course, lab):
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
    def edit_contact_info(self):
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
