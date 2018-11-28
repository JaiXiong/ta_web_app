from django.test import TestCase
from website.models import Course, Account
from ta_app.commands import Commands


class TestCommandsCreateCourse(TestCase):

    def setUp(self):
        self.Course1 = Course.objects.create(name="CS-337",
                                             section="004",
                                             days_of_week="M/W/F",
                                             start_time="11:00",
                                             end_time="11:50",
                                             lab_sections="001/002/003")
        self.Course1.save()
        self.Course2 = Course.objects.create(name="CS-361",
                                             section="003",
                                             days_of_week="T/R",
                                             start_time="12:00",
                                             end_time="13:15")
        self.Course2.save()

    # test for valid number of parameters
    def test_CommandsCreateCourse1(self):
        co = Commands()
        response = co.create_course("CS-458", "001", "T/R", "03:00-04:15")
        self.assertEqual(response, "Please input valid arguments for all fields to create a course")

    # test that duplicate classes are not added to the data base
    def test_CommandsCreateCourse2(self):
        co = Commands()
        response = co.create_course("CS-337", "004", "M/W/F", "11:00-11:50", "001/002/003")
        self.assertEqual(response, "Course CS-337 - 004 already exists in the data base")

    # test that invalid day representation is caught
    def test_CommandsCreateCourse3(self):
        co = Commands()
        response = co.create_course("CS-520", "004", "Z/x", "11:00-11:50", "001/002/003")
        self.assertEqual(response, "Days of week are noted as M, T, W, R, F, S, U, O")

    # test that start times not in range are caught
    def test_CommandsCreateCourse4(self):
        co = Commands()
        response = co.create_course("CS-520", "004", "M/W/F", "24:00-11:50", "001/002/003")
        self.assertEqual(response, "valid start time is 00:00 to 23:59")

    # test that end times not in range are caught
    def test_CommandsCreateCourse5(self):
        co = Commands()
        response = co.create_course("CS-520", "004", "M/W/F", "11:00-24:00", "001/002/003")
        self.assertEqual(response, "valid end time is 00:00 to 23:59")

    # test that end times earlier than start time is caught
    def test_CommandsCreateCourse6(self):
        co = Commands()
        response = co.create_course("CS-520", "004", "M/W/F", "11:00-10:00", "001/002/003")
        self.assertEqual(response, "end time can not be earlier than start time")

    # test that labs sections not a three digit numeric value are caught
    def test_CommandsCreateCourse7(self):
        co = Commands()
        response = co.create_course("CS-520", "004", "M/W/F", "09:00-10:00", "001/0x2/003")
        self.assertEqual(response, "Lab sections must be a three digit number")

    # test that proper call to course adds course to data base
    def test_CommandsCreateCourse8(self):
        co = Commands()
        response = co.create_course("CS-520", "004", "M/W/F", "09:00-10:00", "001/002/003")
        self.assertEqual(response, "Course CS-520 has been added to the data base.")
        count = Course.objects.filter(name="CS-520").count()
        self.assertEqual(count, 1)