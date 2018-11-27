from ta_app.DB_interface import DBConnect
from website.models import Course, Account


class DBConnection(DBConnect):

    def connect(self, db_path: str):
        return True

    def disconnect(self):
        return True

    def add_course(self, entry: Course):
        result = False
        if entry is None:
            return result
        course_name = entry.name
        course_list = list(Course.objects.filter(name=course_name))
        if len(course_list) == 0:
            entry.save()
            result = True
        return result

    def remove_course(self, entry: Course):
        result = False
        if entry is None:
            return result
        course_name = entry.name
        course_list = list(Course.objects.filter(name=course_name))
        if len(course_list) == 1:
            entry.delete()
            result = True
        return result

    def edit_course(self, old_entry: Course, new_entry: Course):
        return False

    def get_courses(self):
        return False

    def add_account(self, entry: Account):
        result = False
        if entry is None:
            return result
        user_list = list(Account.objects.filter(user=entry.user))
        if len(user_list) == 0:
            entry.save()
            result = True
        return result

    def remove_account(self, entry: Account):
        result = False
        if entry is None:
            return result
        user_list = list(Account.objects.filter(user=entry.user))
        if len(user_list) == 1:
            entry.delete()
            result = True
        return result

    def edit_account(self, old_entry: Account, new_entry: Account):
        return False

    def get_accounts(self):
        return False

