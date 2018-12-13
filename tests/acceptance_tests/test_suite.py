import unittest as ut
from tests.acceptance_tests.test_help import TestHelp
from tests.acceptance_tests.test_login import TestLogin
from tests.acceptance_tests.test_logout import TestLogout
from tests.acceptance_tests.test_create_account import TestCreateAccount
from tests.acceptance_tests.test_create_course import TestCreateCourse
from tests.acceptance_tests.test_delete_account import TestDeleteAccount
from tests.acceptance_tests.test_assign_ta_to_course import TestAssignTaToCourse
from tests.acceptance_tests.test_assign_ta_to_lab import TestAssignTaToLab
from tests.acceptance_tests.test_edit_contact_info import TestEditContactInfo
from tests.acceptance_tests.test_view_ta_assignments import TestViewTaAssignments
from tests.acceptance_tests.test_view_course_assignments import TestViewCourseAssignments
from tests.acceptance_tests.test_read_contact_info import TestReadContactInfo


suite = ut.TestSuite()
suite.addTest(ut.makeSuite(TestHelp))
suite.addTest(ut.makeSuite(TestLogin))
suite.addTest(ut.makeSuite(TestLogout))
suite.addTest(ut.makeSuite(TestCreateAccount))
suite.addTest(ut.makeSuite(TestCreateCourse))
suite.addTest(ut.makeSuite(TestDeleteAccount))
suite.addTest(ut.makeSuite(TestAssignTaToCourse))
suite.addTest(ut.makeSuite(TestAssignTaToLab))
suite.addTest(ut.makeSuite(TestEditContactInfo))
suite.addTest(ut.makeSuite(TestViewTaAssignments))
suite.addTest(ut.makeSuite(TestViewCourseAssignments))
suite.addTest(ut.makeSuite(TestReadContactInfo))

runner = ut.TextTestRunner()
res = runner.run(suite)
print(res)
print("*" * 20)
for i in res.failures:
    print(i[1])

if __name__ == '__main__':
    ut.main()