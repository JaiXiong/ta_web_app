import unittest as ut
from tests.unit_tests.test_account_object import TestAccountObject
from tests.unit_tests.test_course_object import TestCourseObject
from tests.unit_tests.test_ui_command import TestUiCommand
from tests.unit_tests.test_superuser_login import TestSuperuserLogin
from tests.unit_tests.test_db_text import TestDBText
from tests.unit_tests.test_ui import TestUI

suite = ut.TestSuite()
suite.addTest(ut.makeSuite(TestAccountObject))
suite.addTest(ut.makeSuite(TestCourseObject))
suite.addTest(ut.makeSuite(TestUiCommand))
suite.addTest(ut.makeSuite(TestSuperuserLogin))
suite.addTest(ut.makeSuite(TestDBText))
suite.addTest((ut.makeSuite(TestUI)))

runner = ut.TextTestRunner()
res = runner.run(suite)
print(res)
print("*" * 20)
for i in res.failures:
    print(i[1])

if __name__ == '__main__':
    ut.main()
