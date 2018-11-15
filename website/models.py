from django.db import models


class Account(models.Model):
    user = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=17)
    street_address = models.CharField(max_length=35)
    email_address = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=12)


class Course(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=3)
    """days_of_week = []"""
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=3)
    instructor = models.ForeignKey(Account, on_delete=models.CASCADE)
    """tas = []"""
    lab = models.CharField(max_length=3)
    """lab_sections = []"""






