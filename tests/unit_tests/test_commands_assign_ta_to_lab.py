from django.test import TestCase
from website.models import Course, Account, Lab
from ta_app.commands import Commands


class TestCommandsAssignTaToLab(TestCase):

    def setUp(self):
        self.Course1 = Course.objects.create(name="CS-337",
                                             section="001",
                                             days_of_week="M/W",
                                             start_time="11:00",
                                             end_time="11:50")
        self.Course1.save()
        self.Course2 = Course.objects.create(name="CS-361",
                                             section="003",
                                             days_of_week="T/R",
                                             start_time="14:00",
                                             end_time="14:50")
        self.Course2.save()
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
                                               role="Supervisor")
        self.Account1.save()

        self.Account2 = Account.objects.create(user="Matt",
                                               password="nonsense",
                                               role="TA")
        self.Account2.save()
        self.Account3 = Account.objects.create(user="Joe",
                                               password="nonsense",
                                               role="TA")
        self.Account3.save()
        self.Course1.tas.add(self.Account3)
        self.Course1.save()
        self.co = Commands()
        self.co.current_user = self.Account1

    # test roles other than supervisor or Instructor can not assign tas to courses
    def test_CommandsAssignTaToLab1(self):
        self.co.current_user = self.Account3
        response = self.co.assign_ta_to_lab('Joe', 'CS-337', "002")
        self.assertEqual("You do not have permissions to assign TAs to labs", response)

    # test assigning a TA to lab without proper arguments
    def test_CommandsAssignTaToLab2(self):
        response = self.co.assign_ta_to_lab()
        self.assertEqual("Please input valid arguments for all fields to assign a TA to a lab section", response)

    # test assigning a user to a lab that's not in the data base
    def test_CommandsAssignTaToLab3(self):
        response = self.co.assign_ta_to_lab('Gus', '337', '003')
        self.assertEqual("This user is not present in the data base", response)

    # test assigning an TA to a lab of a course not in the data base
    def test_CommandsAssignTaToLab4(self):
        response = self.co.assign_ta_to_lab('Joe', 'CS-999', '001')
        self.assertEqual("This course is not present in the data base", response)

    # test assigning a TA to a lab that does not exist for the given course
    def test_CommandsAssignTaToLab5(self):
        response = self.co.assign_ta_to_lab('Joe', 'CS-337', '999')
        self.assertEqual("Course CS-337 does not have lab section 999 present in the data base", response)

    # test assigning a TA to a lab section that is not already assigned to its course
    def test_CommandsAssignTaToLab6(self):
        response = self.co.assign_ta_to_lab('Matt', 'CS-337', '002')
        self.assertEqual("This user is not assigned as a TA to this course", response)

    # test assigning TA to lab that conflicts with their schedule
    def test_CommandsAssignTaToLab7(self):
        self.co.assign_ta_to_course('Joe', 'CS-361')
        response = self.co.assign_ta_to_lab('Joe', 'CS-337', '002')
        self.assertEqual("This lab conflicts with the TA's current schedule", response)

    # test that TA is assigned to lab with proper conditions
    def test_CommandsAssignTaToLab8(self):
        response = self.co.assign_ta_to_lab('Joe', 'CS-337', '002')
        self.assertEqual("Joe has been assigned as the TA to CS-337 002", response)