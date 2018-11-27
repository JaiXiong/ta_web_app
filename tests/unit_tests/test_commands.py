#from django.conf import settings
#settings.configure()
import unittest as ut
from ta_app.commands import Commands
import ta_app.wsgi
from website.models import Account, Course



class TestCommands(ut.TestCase):

    def setUp(self):
        self.ui = Commands()
        self.testUser = Account(user='user', password='password', role='Supervisor')
        self.testUser.save()

    def TestLogin(self):
        pass