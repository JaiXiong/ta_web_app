import unittest as ut
from unittest import mock
from ta_app.course_object import Course


class TestCourseObject(ut.TestCase):

    # test name property
    def test_Course1(self):
        co = Course("CS-337", "004", ["M", "W", "F"], "11:00", "11:50", ["001", "002", "003"])
        co.name = "CS-361"
        self.assertEqual(co.name, "CS-361")

    # test section property
    def test_Course2(self):
        co = Course("CS-337", "004", ["M", "W", "F"], "11:00", "11:50", ["001", "002", "003"])
        co.section = "001"
        self.assertEqual(co.section, "001")

    # test that section property raises an exception with input longer than 3 digits
    def test_Course3(self):
        co = Course("CS-337", "004", ["M", "W", "F"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.section = "00001"
        self.assertEqual("Section must be a three digit number", str(ctx.exception))

    # test that section property only accepts numeric values
    def test_Course4(self):
        co = Course("CS-337", "004", ["M", "W", "F"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.section = "abs"
        self.assertEqual("Section must be a three digit number", str(ctx.exception))

    # test days_of_week property
    def test_Course5(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.days_of_week = ["M", "W", "F"]
        self.assertEqual(co.days_of_week, ["M", "W", "F"])

    # test that days_of_week property raises an exception with invalid day value
    def test_Course6(self):
        with self.assertRaises(ValueError) as ctx:
            co = Course("CS-337", "004", ["T", "Z"], "11:00", "11:50", ["001", "002", "003"])
        self.assertEqual("Days of week are noted as M T W R F", str(ctx.exception))

    # test start_time property
    def test_Course7(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.start_time = "11:00"
        self.assertEqual(co.start_time, "11:00")

    # test that start_time property raises exception with input greater than 23:59
    def test_Course8(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.start_time = "24:00"
        self.assertEqual("valid start time is 00:00 to 23:59", str(ctx.exception))

    # test that start_time property raises error if input is not in form 00:00
    def test_Course9(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.start_time = "23:000"
        self.assertEqual("valid start time is 00:00 to 23:59", str(ctx.exception))

    # test end_time property
    def test_Course10(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.end_time = "11:00"
        self.assertEqual(co.end_time, "11:00")

    # test that end_time property raises exception with input greater than 23:59
    def test_Course11(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.end_time = "24:00"
        self.assertEqual("valid end time is 00:00 to 23:59", str(ctx.exception))

    # test that end_time property if input is not in form 00:00
    def test_Course12(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.end_time = "23:000"
        self.assertEqual("valid end time is 00:00 to 23:59", str(ctx.exception))

    # test that end time property is greater that start time property
    def test_Course13(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.start_time = "11:00"
        with self.assertRaises(ValueError) as ctx:
            co.end_time = "10:00"
        self.assertEqual("end time can not be earlier than start time", str(ctx.exception))

    # test instructor properties
    def test_Course14(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.instructor = " Jason Rock"
        self.assertEqual(co.instructor, " Jason Rock")

    # test tas properties
    def test_Course15(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.tas = ["Steve", "Tim"]
        self.assertEqual(co.tas, ["Steve", "Tim"])

    # test lab properties
    def test_Course16(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.lab = "008"
        self.assertEqual(co.lab, "008")

    # test that lab property raises an exception with input longer than 3 digits
    def test_Course17(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.lab = "00001"
        self.assertEqual("Lab must be a three digit number", str(ctx.exception))

    # test that lab property only accepts numeric values
    def test_Course18(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.lab = "abs"
        self.assertEqual("Lab must be a three digit number", str(ctx.exception))

    # test lab_sections property
    def test_Course19(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        co.lab_sections = ["008", "009"]
        self.assertEqual(co.lab_sections, ["008", "009"])

    # test that lab_sections property raises an exception with input longer than 3 digits
    def test_Course20(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.lab_sections = ["00001"]
        self.assertEqual("Lab sections must be a three digit number", str(ctx.exception))

    # test that lab_sections property only accepts numeric values
    def test_Course21(self):
        co = Course("CS-337", "004", ["M", "W"], "11:00", "11:50", ["001", "002", "003"])
        with self.assertRaises(ValueError) as ctx:
            co.lab_sections = ["abs", "001", "r34"]
        self.assertEqual("Lab sections must be a three digit number", str(ctx.exception))

    # test Course constructor
    def test_Course22(self):
        co = Course("CS-361", "001", ["T", "R"], "11:00", "11:50", ["001", "002", "003"])
        self.assertEqual(co.name, "CS-361")
        self.assertEqual(co.section, "001")
        self.assertEqual(co.days_of_week, ["T", "R"])
        self.assertEqual(co.start_time, "11:00")
        self.assertEqual(co.end_time, "11:50")
        self.assertEqual(co.lab_sections, ["001", "002", "003"])
