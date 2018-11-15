import unittest as ut
from unittest import mock
from ta_app.ui import UI
from ta_app.course_object import Course


class TestUiCreateCourse(ut.TestCase):

    def setUp(self):
        self.uio = UI()

    # test that create_course calls Course constructor with proper parameters
    def test_UiCreateCourse1(self):
        patcher = mock.patch.object(Course, "__init__")
        patched = patcher.start()
        self.uio.create_course("CS-337", "004", "M/W/F", "11:00-11:50", "001/002/003")
        assert patched.call_count == 1
        patched.assert_called_with("CS-337", "004", ["M", "W", "F"], "11:00", "11:50", ["001", "002", "003"])

    # test that create_course raises an error if all required parameters are not passed in
    def test_UiCreateCourse2(self):
        with self.assertRaises(ValueError) as ctx:
            self.uio.create_course("CS-337")
        self.assertEqual("Please fill in all required fields to create a course", str(ctx.exception))

