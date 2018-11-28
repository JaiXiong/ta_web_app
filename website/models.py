from django.db import models
from ta_app.course_interface import ICourse


class Account(models.Model):
    user = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=17)
    street_address = models.CharField(max_length=35, blank=True)
    email_address = models.EmailField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=3)
    days_of_week = models.CharField(max_length=8)
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=3)
    instructor = models.ForeignKey(Account, related_name="instructor", on_delete=models.CASCADE, null=True)
    tas = models.ManyToManyField(Account, related_name="tas", blank=True)
    lab = models.CharField(max_length=3, null=True)
    lab_sections = models.CharField(max_length=3, null=True)







