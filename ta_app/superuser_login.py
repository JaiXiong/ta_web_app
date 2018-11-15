from ta_app.db_connect_object import DBConnection
from ta_app.account_object import Account


class Superuser:

    # hard coded
    __name = "default_superuser"
    __password = "default_password"
    __role = "default_superuser"

    def __init__(self):
        pass
        # db = DBConnection()
        # account = Account()
        # dbpath = db.db_path()

    def superuser_authentication(self, name, password):
        if name is None or password is None:
            print("login failed. Invalid username or password")
            return False
        elif name == self.__name and password == self.__password:
            # design task, do we add superuser to a account?
            # if so, Superuser class needs access to the database/txtfile
            # therefore, needs to be able to first read from a txtfile
            # then later access to the database
            # therefore, I think we should always check to make sure this user has superuser 'role'
            # so for now, default check to make sure role is always 'default_superuser', which is always true
            # with open("users.txt", "r") as file:
              #  data = file.read()
               # for line in data:
                #    word1, word2, word3 = data.split(",")

                 #   if check_name(word1) is True:
                  #      if check_password(word2) is True:
                   #         if check_role(word3) is True:
                    #            print("login as " + name)
                     #           return True
            print("login as " + name)
            return True
        else:
            print("login failed. Invalid username or password")
            return False

    def check_name(self, name):
        if name == self.__name:
            return True
        else:
            print("login failed. Invalid username or password")
            return False

    def check_password(self, password):
        if password == self.__password:
            return True
        else:
            print("login failed. Invalid username or password")
            return False

    def check_role(self, role):
        if role == self.__role:
            return True
        else:
            print("login failed. Invalid username or password")
            return False
