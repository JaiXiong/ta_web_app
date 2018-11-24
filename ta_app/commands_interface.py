import abc


class CommandsInterface(abc.ABC):

    @abc.abstractmethod
    def login(self, user, password):
        pass

    @abc.abstractmethod
    def logout(self):
        pass

    @abc.abstractmethod
    def create_course(self, name, section, days, times, labs):
        pass

    @abc.abstractmethod
    def create_account(self, user, password, role):
        pass

    @abc.abstractmethod
    def delete_account(self, user, password, role):
        pass

    @abc.abstractmethod
    def edit_account(self, user):
        pass

    @abc.abstractmethod
    def assign_instructor(self, user, course):
        pass

    @abc.abstractmethod
    def assign_ta_to_course(self, user, course):
        pass

    @abc.abstractmethod
    def assign_ta_to_lab(self, user, course, lab):
        pass

    @abc.abstractmethod
    def read_contact_info(self):
        pass

    @abc.abstractmethod
    def edit_contact_info(self):
        pass

    @abc.abstractmethod
    def view_course_assignments(self):
        pass

    @abc.abstractmethod
    def view_ta_assignments(self):
        pass

    @abc.abstractmethod
    def help(self):
        pass

    @abc.abstractmethod
    def get_current_user(self):
        pass

    @abc.abstractmethod
    def call_command(self, command):
        pass
