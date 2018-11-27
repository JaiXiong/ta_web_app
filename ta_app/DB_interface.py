import abc
from website.models import Course, Account


class DBConnect(abc.ABC):

    @abc.abstractmethod
    def connect(self, db_path: str) -> bool:
        pass

    @abc.abstractmethod
    def disconnect(self) -> bool:
        pass

    @abc.abstractmethod
    def add_course(self, entry: Course) -> bool:
        pass

    @abc.abstractmethod
    def remove_course(self, entry: Course) -> bool:
        pass

    @abc.abstractmethod
    def edit_course(self, old_entry: Course, new_entry: Course) -> bool:
        pass

    @abc.abstractmethod
    def get_courses(self) -> list:
        pass

    @abc.abstractmethod
    def add_account(self, entry: Account) -> bool:
        pass

    @abc.abstractmethod
    def remove_account(self, entry: Account) -> bool:
        pass

    @abc.abstractmethod
    def edit_account(self, old_entry: Account, new_entry: Account) -> bool:
        pass

    @abc.abstractmethod
    def get_accounts(self) -> list:
        pass
