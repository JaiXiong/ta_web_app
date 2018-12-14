from django.test import TestCase
from ta_app.commands import Commands
import ta_app.wsgi
from website.models import Account, Course


class TestViewCourseAssignments(TestCase):

    def setUp(self):
        self.ui = Commands()
        self.tst_supervisor = Account(user='usrSupervisor', password='password', role='Supervisor')
        self.tst_administrator = Account(user='usrAdministrator', password='password', role='Administrator')
        self.tst_instructor = Account(user='usrInstructor', password='password', role='Instructor')
        self.tst_ta = Account(user='usrTA', password='password', role='TA')
        self.tst_supervisor.save()
        self.tst_administrator.save()
        self.tst_instructor.save()
        self.tst_ta.save()

    def test_view_course_assignments_no_user(self):
        expected_output = "Failed to view course assignments. No current user"
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_course_assignments_as_ta(self):
        self.ui.login('usrTA', 'password')
        expected_output = "Failed to view course assignments. Insufficient permissions"
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_course_assignments_as_instructor(self):
        self.ui.login('usrInstructor', 'password')
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_course_assignments_as_supervisor(self):
        self.ui.login('usrSupervisor', 'password')
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_course_assignments_as_Administrator(self):
        self.ui.login('usrAdministrator', 'password')
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_course_assignments_multiple_courses_multiple_instructors_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        test_instructor2 = Account(user='usrInstructor2', password='password', role='Instructor')
        test_instructor2.save()
        test_course1 = Course(name="CS103",
                              section="222",
                              days_of_week="M/W/F",
                              start_time="12:00",
                              end_time="13:00",
                              instructor=self.tst_instructor,
                              lab="333")
        test_course1.save()
        test_course2 = Course(name="CS104",
                              section="223",
                              days_of_week="M/W/F",
                              start_time="14:00",
                              end_time="15:00",
                              instructor=test_instructor2,
                              lab="363")
        test_course2.save()
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_course_assignments_no_instructor_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             lab="333")
        test_course.save()
        test_course2 = Course(name="CS104",
                              section="223",
                              days_of_week="M/W/F",
                              start_time="14:00",
                              end_time="15:00",
                              instructor=self.tst_instructor,
                              lab="363")
        test_course2.save()
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_course_assignments()
        self.assertEqual(expected_output, actual_output)

    # =====================================================================
    def test_view_ta_assignments_no_user(self):
        expected_output = "Failed to view ta assignments. No current user"
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_ta_assignments_single_ta_single_course_as_ta(self):
        self.ui.login("usrTA", "password")
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        test_course.tas.add(self.tst_ta)
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_ta_assignments_single_ta_single_course_as_instructor(self):
        self.ui.login("usrInstructor", "password")
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        test_course.tas.add(self.tst_ta)
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_ta_assignments_single_ta_single_course_as_supervisor(self):
        self.ui.login("usrSupervisor", "password")
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        test_course.tas.add(self.tst_ta)
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_ta_assignments_single_ta_single_course_as_administrator(self):
        self.ui.login("usrAdministrator", "password")
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        test_course.tas.add(self.tst_ta)
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_ta_assignments_multiple_ta_single_course_as_ta(self):
        self.ui.login("usrTA", "password")
        test_ta2 = Account(user="TA2", password="password", role="TA")
        test_ta2.save()
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        test_course.tas.add(self.tst_ta)
        test_course.tas.add(test_ta2)
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)

    def test_view_ta_assignments_single_ta_multiple_course_as_ta(self):
        self.ui.login("usrTA", "password")
        test_ta2 = Account(user="TA2", password="password", role="TA")
        test_ta2.save()
        test_course = Course(name="CS103",
                             section="222",
                             days_of_week="M/W/F",
                             start_time="12:00",
                             end_time="13:00",
                             instructor=self.tst_instructor,
                             lab="333")
        test_course.save()
        test_course.tas.add(self.tst_ta)
        test_course2 = Course(name="CS104",
                              section="223",
                              days_of_week="M/W/F",
                              start_time="14:00",
                              end_time="15:00",
                              instructor=self.tst_instructor,
                              lab="363")
        test_course2.save()
        test_course2.tas.add(test_ta2)
        expected_output = list(Course.objects.all())
        actual_output = self.ui.view_ta_assignments()
        self.assertEqual(expected_output, actual_output)
