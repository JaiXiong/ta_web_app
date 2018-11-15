from ta_app.DB_interface import DBConnect
import os.path
from ta_app.account_object import Account
from ta_app.course_object import Course


class DBConnection(DBConnect):
    __dbPath: str = ""
    __isConnected: bool = False
    __dbObject = None

    def __init__(self):
        self.__dbPath = ""
        self.__isConnected = False
        self.__dbObject = None

    @property
    def is_connected(self):
        return self.__isConnected

    @property
    def db_path(self):
        return self.__dbPath

    @property
    def db_object(self):
        return self.__dbObject

    def connect(self, db_path: str = "") -> bool:
        """
        :param db_path: the path to the database file
        :return: a boolean if connection was successful
        """
        # First we check if the path has actual text in it, then look to see
        #   if it's an actual file on disk
        if db_path == "" or not os.path.isfile(db_path):
            return False
        try:
            self.__dbObject = open(db_path)
        except OSError as ose:
            print(ose + " DBConnection (connect) Could not find file with given path: " + db_path)
            return False
        # Once the file has been opened to create a pointer its immediately closed
        #   for other functions, the path is set, and a boolean is set saying we connected
        self.__dbObject.close()
        self.__dbPath = db_path
        self.__isConnected = True
        return True

    def disconnect(self) -> bool:
        """
        :return: a boolean if the connection object was successfully disconnected
        """
        if self.db_object is None:
            return False
        # Double check this so nothing leaks
        if not self.db_object.closed:
            self.db_object.close()
        # set the members to reflect a disconnect from the DB and no active path
        self.__dbObject = None
        self.__dbPath = ""
        self.__isConnected = False
        return True

    def add_account(self, entry: Account) -> bool:
        """
        :param entry: a data validated Account object that will entered into the DB
        :return: a boolean if the process was successful
        """
        self.__dbObject = open(self.db_path, "a+")
        if self.db_object is None or entry is None or not self.__isConnected:
            return False
        self.db_object.write(entry.__str__() + "\n")
        self.__dbObject.close()
        return True

    def remove_account(self, entry: Account) -> bool:
        """
        :param entry: a data validated Account object to be deleted from the DB
        :return:
        """
        if not self.__isConnected:
            return False
        self.__dbObject = open(self.db_path, "r")
        search_entry = entry.__str__() + "\n"
        account_list = self.db_object.readlines()
        if entry is None or search_entry not in account_list:
                return False
        self.db_object.close()
        # The file has to be reopened in the same method to perform the write operations
        self.__dbObject = open(self.db_path, "a")
        # this truncate operation empties a file,
        #   I can't do a line specific remove/insert
        self.db_object.truncate(0)
        for account in account_list:
            if account != search_entry:
                self.db_object.write(account.__str__() + "\n")
        self.db_object.close()
        return True

    def edit_account(self, old_entry: Account, new_entry: Account) -> bool:
        return True

    def add_course(self, entry: Course) -> bool:
        """
            :param entry: a data validated Course object that will entered into the DB
            :return: a boolean if the process was successful
        """
        self.__dbObject = open(self.db_path, "a+")
        if self.db_object is None or entry is None or not self.__isConnected:
            return False
        self.db_object.write(entry.__str__() + "\n")
        self.__dbObject.close()
        return True

    def remove_course(self, entry: Course) -> bool:
        return True

    def edit_course(self, old_entry: Course, new_entry: Course) -> bool:
        return True

    def get_accounts(self) -> list:
        return []

    def get_courses(self) -> list:
        return []
