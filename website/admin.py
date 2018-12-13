from django.contrib import admin

# Register your models here.
from .models import Account, Course, Lab
admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Lab)
