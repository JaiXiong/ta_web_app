import abc


class IAccount:

    @abc.abstractmethod
    def user(self, u):
        pass

    @abc.abstractmethod
    def password(self, p):
        pass

    @abc.abstractmethod
    def role(self, r):
        pass

    @abc.abstractmethod
    def street_address(self, a):
        pass

    @abc.abstractmethod
    def email_address(self, e):
        pass

    @abc.abstractmethod
    def phone_number(self, p):
        pass
