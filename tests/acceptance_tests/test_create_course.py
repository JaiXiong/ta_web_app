#Gus
import unittest as ut
from ta_app.ui import UI


class TestCreateCourse(ut.TestCase):

    def setUp(self):
        self.ui = UI()

    # tests if a course with valid parameters is correctly created
    def testCreateCourse1(self):
        self.ui.command("login defaultuser defaultpassword")
        result0 = self.ui.command("create_course defaultName 001 M/W/F 9:00AM-9:50AM 801")
        self.assertEquals(result0, "course: defaultName, section: 001, meeting: M/W/F 9:00AM-9:50AM, section: 801, has been created")
        self.ui.command("logout")

    # tests that a course created with incorrect parameters returns an error
    def testCreateCourse2(self):
        self.ui.command("login defaultuser defaultpassword")
        result1 = self.ui.command("create_course beans broccoli spinach cabbage celery")
        self.assertEquals(result1, "Please input valid arguments for all fields to create a course")
        self.ui.command("logout")

    # tests that a course created with blank/missing parameters returns an error
    def testCreateCourse3(self):
        self.ui.command("login defaultuser defaultpassword")
        result2 = self.ui.command("create_course defaultName1 001 M/W/F")
        self.assertEquals(result2, "Please input valid arguments for all fields to create a course")
        self.ui.command("logout")

    # tests that a course that already exists cannot be created again
    def testCreateCourse4(self):
        self.ui.command("login defaultuser defaultpassword")
        self.ui.command("create_course defaultName3 003 T/R 10:00AM-10:50AM 803")
        result3 = self.ui.command("create_course defaultName3 001 M/W/F 9:00AM-9:50AM 801")
        self.assertEquals(result3, "Course already exists in the database")
        self.ui.command("logout")
