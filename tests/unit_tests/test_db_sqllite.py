from django.test import TestCase
from website import models
from ta_app.db_connect_sqllite import DBConnection


class TestDBSqlLite(TestCase):

    def setUp(self):
        self.db_connection = DBConnection()
        self.Account1 = models.Account(user="user",
                                       password="password",
                                       role="TA",
                                       street_address="123 N. Lol Drive",
                                       email_address="test@uwm.edu",
                                       phone_number="6081234567")
        self.Course1 = models.Course(name="CS103",
                                     section="222",
                                     start_time="12:00",
                                     end_time="13:00",
                                     instructor=self.Account1,
                                     lab="333")

############################################################

    def test_add_account_Successful(self):
        self.assertTrue(self.db_connection.add_account(self.Account1))
        lsAccount = list(models.Account.objects.filter(user=self.Account1.user,
                                                       password=self.Account1.password,
                                                       role=self.Account1.role,
                                                       street_address=self.Account1.street_address,
                                                       email_address=self.Account1.email_address,
                                                       phone_number=self.Account1.phone_number)
                         )
        self.assertEqual(len(lsAccount), 1)

    def test_add_account_None(self):
        self.assertFalse(self.db_connection.add_account(None))

    def test_remove_account_Successful(self):
        self.assertTrue(self.db_connection.add_account(self.Account1))
        lsAccount = list(models.Account.objects.filter(user=self.Account1.user,
                                                       password=self.Account1.password,
                                                       role=self.Account1.role,
                                                       street_address=self.Account1.street_address,
                                                       email_address=self.Account1.email_address,
                                                       phone_number=self.Account1.phone_number)
                         )
        self.assertEqual(len(lsAccount), 1)
        self.assertTrue(self.db_connection.remove_account(self.Account1))
        lsAccount = list(models.Account.objects.filter(user=self.Account1.user,
                                                       password=self.Account1.password,
                                                       role=self.Account1.role,
                                                       street_address=self.Account1.street_address,
                                                       email_address=self.Account1.email_address,
                                                       phone_number=self.Account1.phone_number)
                         )
        self.assertEqual(len(lsAccount), 0)

    def test_remove_account_None(self):
        self.assertFalse(self.db_connection.remove_account(None))

    def test_remove_account_NoExistAccount(self):
        self.assertTrue(self.db_connection.add_account(self.Account1))
        account2 = models.Account(user = "user2",
                                  password = "password2",
                                  role = "Administrator"
                                  )
        self.assertFalse(self.db_connection.remove_account(account2))
############################################################

    def test_add_course_Successful(self):
        self.Account1.save()
        self.assertTrue(self.db_connection.add_course(self.Course1))
        lsCourse = list(models.Course.objects.filter(name=self.Course1.name,
                                                     section=self.Course1.section,
                                                     start_time=self.Course1.start_time,
                                                     end_time=self.Course1.end_time,
                                                     )
                        )
        self.assertEqual(len(lsCourse), 1)

    def test_add_course_None(self):
        self.assertFalse(self.db_connection.add_course(None))

    def test_remove_course_Successful(self):
        self.Account1.save()
        self.assertTrue(self.db_connection.add_course(self.Course1))
        lsCourse = list(models.Course.objects.filter(name=self.Course1.name,
                                                     section=self.Course1.section,
                                                     start_time=self.Course1.start_time,
                                                     end_time=self.Course1.end_time,
                                                     )
                        )
        self.assertEqual(len(lsCourse), 1)
        self.assertTrue(self.db_connection.remove_course(self.Course1))
        lsCourse = list(models.Course.objects.filter(name=self.Course1.name,
                                                     section=self.Course1.section,
                                                     start_time=self.Course1.start_time,
                                                     end_time=self.Course1.end_time,
                                                     )
                        )
        self.assertEqual(len(lsCourse), 0)

    def test_remove_account_None(self):
        self.assertFalse(self.db_connection.remove_course(None))

    def test_remove_account_NoExistCourse(self):
        self.Account1.save()
        self.assertTrue(self.db_connection.add_course(self.Course1))
        course2 = models.Course(name = "CS104",
                                section = "242",
                                start_time = "14:00",
                                end_time = "15:00",
                                instructor = self.Account1,
                                lab = "336"
                                )
        self.assertFalse(self.db_connection.remove_course(course2))






