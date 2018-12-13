class Course:
    __name = ""
    __section = ""
    __days_of_week = []
    __start_time = "00:00"
    __end_time = "00:00"
    __instructor = ""
    __tas = []
    __lab = ""
    __lab_sections = []

    def __init__(self, coursename, sec, days, stime, etime, labsec=[]):
            self.name = coursename
            self.section = sec
            self.days_of_week = days
            self.start_time = stime
            self.end_time = etime
            self.lab_sections = labsec

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, n):
        self.__name = n

    @property
    def section(self, ):
        return self.__section

    @section.setter
    def section(self, s):
            if len(s) > 3 or not s.isnumeric():
                raise ValueError("Section must be a three digit number")
            else:
                self.__section = s

    @property
    def days_of_week(self):
        return self.__days_of_week

    @days_of_week.setter
    def days_of_week(self, d):
        valid = True
        for day in d:
            if day not in ["M", "T", "W", "R", "F", "S", "U", "O"]:
                valid = False
                raise ValueError("Days of week are noted as M T W R F")

        if valid:
            self.__days_of_week = d

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, s):
        stl = s.split(":")
        if len(s) > 5 or s[2] != ":" or int(stl[0]) > 23 or int(stl[1]) > 59:
            raise ValueError("valid start time is 00:00 to 23:59")
        else:
            self.__start_time = s

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, e):
        etl = e.split(":")
        stl = self.__start_time.split(":")
        if len(e) > 5 or e[2] != ":" or int(etl[0]) > 23 or int(etl[1]) > 59:
            raise ValueError("valid end time is 00:00 to 23:59")
        elif stl[0] > etl[0] or (stl[0] == etl[0] and stl[1] > etl[1]):
            raise ValueError("end time can not be earlier than start time")
        else:
            self.__end_time = e

    @property
    def instructor(self):
        return self.__instructor

    @instructor.setter
    def instructor(self, i):
        self.__instructor = i

    @property
    def tas(self):
        return self.__tas

    @tas.setter
    def tas(self, ts):
        self.__tas = ts

    @property
    def lab(self):
        return self.__lab

    @lab.setter
    def lab(self, l):
        if len(l) > 3 or not l.isnumeric():
            raise ValueError("Lab must be a three digit number")
        else:
            self.__lab = l

    @property
    def lab_sections(self):
        return self.__lab_sections

    @lab_sections.setter
    def lab_sections(self, ls):
        valid = True
        for lab in ls:
            if len(lab) > 3 or not lab.isnumeric():
                valid = False
                raise ValueError("Lab sections must be a three digit number")

        if valid:
            self.__lab_sections = ls

    def __str__(self):
        d = ""
        for day in self.days_of_week:
            if day == self.days_of_week[len(self.days_of_week)-1]:
                d += day
            else:
                d += day + "/"

        t = ""
        for ta in self.tas:
            if ta == self.tas[len(self.tas-1)]:
                t += ta
            else:
                t += ta + "/"

        ls = ""
        for lab in self.lab_sections:
            if lab == self.lab_sections[len(self.lab_sections)-1]:
                ls += lab
            else:
                ls += lab + "/"

        return self.name + ", " + self.section + ", " + d + ", " + self.start_time + ", " + self.end_time + ", " + \
            self.instructor + ", " + t + ", " + self.lab + ", " + ls


