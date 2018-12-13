from django.test import TestCase
from website.models import Course, Account, Lab


class TestLabModel(TestCase):

    def setUp(self):

        self.Course1 = Course.objects.create(name="CS-337",
                                             section="001",
                                             days_of_week="M/W",
                                             start_time="11:00",
                                             end_time="11:50")
        self.Course1.save()
        self.Lab1 = Lab.objects.create(course=self.Course1,
                                       section="002",
                                       days_of_week="T",
                                       start_time="14:00",
                                       end_time="15:50")
        self.Lab1.save()

        self.Lab2 = Lab.objects.create(course=self.Course1,
                                       section="003",
                                       days_of_week="F",
                                       start_time="12:00",
                                       end_time="13:50")
        self.Lab2.save()

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

    # test courses are set with proper input
    def test_LabModel1(self):
        self.assertEqual(self.Lab1.course, self.Course1)
        self.assertEqual(self.Lab2.course, self.Course1)

    # test sections are set with proper inputs
    def test_LabModel2(self):
        self.assertEqual(self.Lab1.section, "002")
        self.assertEqual(self.Lab2.section, "003")

    # test days_of_week are set with proper inputs
    def test_LabModel3(self):
        self.assertEqual(self.Lab1.days_of_week, "T")
        self.assertEqual(self.Lab2.days_of_week, "F")

    # test start_time are set with proper inputs
    def test_LabModel3(self):
        self.assertEqual(self.Lab1.start_time, "14:00")
        self.assertEqual(self.Lab2.start_time, "12:00")

    # test end_time are set with proper inputs
    def test_LabModel3(self):
        self.assertEqual(self.Lab1.end_time, "15:50")
        self.assertEqual(self.Lab2.end_time, "13:50")

    # test assigning ta's to Lab
    def test_LabModel3(self):
        self.Course1.tas.add(self.Account2)
        self.Course1.tas.add(self.Account3)
        self.Lab1.ta = self.Account2
        self.Lab2.ta = self.Account3
        self.assertEqual(self.Lab1.ta, self.Account2)
        self.assertEqual(self.Lab2.ta, self.Account3)