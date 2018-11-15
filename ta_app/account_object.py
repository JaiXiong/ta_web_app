class Account:
    __user = ""
    __password = ""
    __role = ""
    __street_address = ""
    __email_address = ""
    __phone_number = ""

    def __init__(self, user, password, role):
        self.user = user
        self.password = password
        self.role = role

    @property
    def user(self):
        return self.__user

    @property
    def password(self):
        return self.__password

    @property
    def role(self):
        return self.__role

    @property
    def address(self):
        return self.address

    @property
    def email_address(self):
        return self.__email_address

    @property
    def phone_number(self):
        return self.__phone_number

    @user.setter
    def user(self, u):
        if u:
            self.__user = u
        else:
            raise ValueError("User cannot be blank")

    @password.setter
    def password(self, p):
        if p:
            self.__password = p
        else:
            raise ValueError("Password cannot be blank")

    @role.setter
    def role(self, r):
        if r not in["Supervisor", "Administrator", "Instructor", "TA", "default_superuser"]:
            raise ValueError("Role is not one of Supervisor, Administrator, Instructor, TA")
        self.__role = r

    @address.setter
    def street_address(self, a):
        if a:
            self.__street_address = a
        else:
            raise ValueError("Address cannot be blank")

    @email_address.setter
    def email_address(self, e):
        if e:
            self.__email_address = e
        else:
            raise ValueError("Email address cannot be blank")

    @phone_number.setter
    def phone_number(self, p):
        if p:
            self.__phone_number = p
        else:
            raise ValueError("Phone number cannot be blank")

    def __str__(self):
        to_str = self.__user + ", " + self.__password + ", " + self.__role + ", " + self.__street_address + ", " + self.__email_address + ", " + self.__phone_number
        return to_str
