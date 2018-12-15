import unittest
from unittest.loader import makeSuite
from tests.unit_tests.test_commands import TestCommands
from tests.unit_tests.test_commands_assign_instructor import TestCommandsAssignInstructor
from tests.unit_tests.test_commands_assign_ta_to_course import TestCommandsAssignTaToCourse
from tests.unit_tests.test_commands_assign_ta_to_lab import TestCommandsAssignTaToLab
from tests.unit_tests.test_commands_create_course import TestCommandsCreateCourse
from tests.unit_tests.test_commands_edit_account import TestEditAccount
from tests.unit_tests.test_commands_edit_contact_info import TestEditContactInfo
"""from tests.unit_tests.test_commands_view_course_assignments import TestViewCourseAssignments"""
from tests.unit_tests.test_commands_read_contact_info import TestReadContactInfo

suite = unittest.TestSuite()
suite.addTest(makeSuite(TestCommands))
suite.addTest(makeSuite(TestCommandsAssignInstructor))
suite.addTest(makeSuite(TestCommandsAssignTaToCourse))
suite.addTest(makeSuite(TestCommandsAssignTaToLab))
suite.addTest(makeSuite(TestCommandsCreateCourse))
suite.addTest(makeSuite(TestEditAccount))
suite.addTest(makeSuite(TestEditContactInfo))
"""suite.addTest(makeSuite(TestViewCourseAssignments))"""
suite.addTest(makeSuite(TestReadContactInfo))

runner = unittest.TextTestRunner()
res = runner.run(suite)
print(res)
print("*" * 20)
for i in res.failures:
    print(i[1])

if __name__ == '__main__':
    unittest.main()
