from django.test import TestCase
from website.models import Course, Account


class TestCourseModel(TestCase):

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

        self.Account1 = Account.objects.create(user="Ross",
                                               password="nonsense",
                                               role="Instructor")
        self.Account1.save()

        self.Account2 = Account.objects.create(user="Matt",
                                               password="nonsense",
                                               role="TA")
        self.Account2.save()

        self.Account3 = Account.objects.create(user="Joe",
                                               password="nonsense",
                                               role="TA")
        self.Account3.save()


    # test name is set with proper inputs
    def test_CourseModel1(self):
        self.assertEqual(self.Course1.name, "CS-337")
        self.assertEqual(self.Course2.name, "CS-361")

    # test section is set with proper inputs
    def test_CourseModel2(self):
        self.assertEqual(self.Course1.section, "004")
        self.assertEqual(self.Course2.section, "003")

    # test days_of_week is set with proper inputs
    def test_CourseModel3(self):
        self.assertEqual(self.Course1.days_of_week, "M/W/F")
        self.assertEqual(self.Course2.days_of_week, "T/R")

    # test start_time is set with proper inputs
    def test_CourseModel4(self):
        self.assertEqual(self.Course1.start_time, "11:00")
        self.assertEqual(self.Course2.start_time, "12:00")

    # test end_time is set with proper inputs
    def test_CourseModel5(self):
        self.assertEqual(self.Course1.end_time, "11:50")
        self.assertEqual(self.Course2.end_time, "13:15")

    # test lab_sections is set with proper inputs
    def test_CourseModel6(self):
        self.assertEqual(self.Course1.lab_sections, "001/002/003")
        self.assertEqual(self.Course2.lab_sections, None)

    # test setting instructor field
    def test_CourseModel7(self):
        self.Course1.instructor = self.Account1
        self.assertEqual(self.Course1.instructor.user, "Ross")

    # test setting lab_sections field
    def test_CourseModel8(self):
        self.Course1.tas.add(self.Account2)
        self.Course1.tas.add(self.Account3)
        ta_query1 = self.Course1.tas.all()
        ta_query2 = self.Course1.tas.get(user="Joe")
        self.assertEqual(ta_query1.count(), 2)
        self.assertEqual(ta_query2.user, "Joe")
