from django.test import TestCase
from website.models import Course, Account
from ta_app.commands import Commands


class TestCommandsAssignInstructor(TestCase):

    def setUp(self):
        self.Course1 = Course.objects.create(name="CS-337",
                                             section="004",
                                             days_of_week="M/W/F",
                                             start_time="11:00",
                                             end_time="11:50")
        self.Course1.save()
        self.Course2 = Course.objects.create(name="CS-361",
                                             section="003",
                                             days_of_week="M/W",
                                             start_time="11:00",
                                             end_time="13:15")
        self.Course2.save()
        self.Account1 = Account.objects.create(user="Ross",
                                               password="nonsense",
                                               role="Supervisor")
        self.Account1.save()
        self.Account2 = Account.objects.create(user="Joe",
                                               password="nonsense",
                                               role="Instructor")
        self.Account2.save()
        self.co = Commands()
        self.co.current_user = self.Account1

    # test roles other than supervisor can not assign instructors
    def test_CommandsAssignInstructor1(self):
        self.co.current_user = Account()
        response = self.co.assign_instructor('Joe', 'CS-361')
        self.assertEqual(response, "You do not have permissions to assign instructors to courses")

    # test assigning a user not in the data base
    def test_CommandsAssignInstructor2(self):
        response = self.co.assign_instructor('Gus', 'CS-361')
        self.assertEqual(response, "This user is not present in the data base")

    # test assigning an instructor to course not in the data base
    def test_CommandsAssignInstructor3(self):
        response = self.co.assign_instructor('Joe', 'CS-999')
        self.assertEqual(response, "This course is not present in the data base")

    # test assigning instructor to course that conflicts with their schedule
    def test_CommandsAssignInstructor4(self):
        self.co.assign_instructor('Joe', 'CS-337')
        response = self.co.assign_instructor('Joe', 'CS-361')
        self.assertEqual(response, "This course conflicts with the instructor's current schedule")

    # test calling method without all valid parameters
    def test_CommandsAssignInstructor5(self):
        response = self.co.assign_instructor('Joe')
        self.assertEqual(response, "Please input valid arguments for both fields to create assign an instructor to a "
                                   "course")

    # test that instructor is added to course wit proper conditions
    def test_CommandsAssignInstructor6(self):
        response = self.co.assign_instructor('Joe', 'CS-361')
        self.assertEqual(response, 'Joe has been added to as CS-361s instructor')
        assigned = Course.objects.filter(name='CS-361', instructor=self.Account2).exists()
        self.assertEqual(True, assigned)

