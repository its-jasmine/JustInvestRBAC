'''
Author: Jasmine Gad El Hak
Exercise: 3 (c)

Description:
Test your enrolment mechanism and proactive password checker.
'''
import unittest
from Problem3a import *
from Problem3b import *
from TEST_CONSTANTS import *



class TestUserEnrollment(unittest.TestCase):
    def setUp(self):
        rbac = RoleBasedAccessControl(TEST_ROLES_AND_OPERATIONS_FILE)
        self.enrolUI = EnrolUserInterface(
            rbac_system=rbac,
            password_file_manager=PasswordFileManager(password_file=TEST_PASSWORD_FILE,
                                hash_function=HASH_FUNCTION,
                                hash_length=HASH_LENGTH,
                                salt_length=SALT_LENGTH,
                                iteration_count=ITERATION_COUNT),
            password_checker=ProactivePasswordChecker(weak_passwords_file=TEST_WEAK_PASSWORDS),
        user_role_file_manager=UserRoleFileManager(TEST_USER_ROLES_FILE))
        self.Role = rbac.Role

    def tearDown(self):
        os.remove(TEST_PASSWORD_FILE)

    def test_user_enrollment(self):
        """Test if a user can be successfully enrolled."""
        username = "test"
        password = "SecurePassword123!"
        result = self.enrolUI.enroll_user(username, password, self.Role("Client"))
        self.assertTrue(result, "User should be successfully enrolled.")

    def test_duplicate_user_enrollment(self):
        """Test if duplicate usernames are prevented."""
        username = "test"
        password = "SecurePassword123!"
        self.enrolUI.enroll_user(username, password, self.Role("Client"))
        result = self.enrolUI.enroll_user(username, "AnotherPassword123!", self.Role("Client"))
        self.assertFalse(result, "Duplicate usernames should not be allowed.")

class TestProactivePasswordChecker(unittest.TestCase):
    def setUp(self):
        self.checker = ProactivePasswordChecker(TEST_WEAK_PASSWORDS)

    def test_check_valid_password(self):
        '''Tests that password validation against defined policy is working as expected'''
        self.assertTrue(self.checker.check_password("test", "123AbC!*"), "123AbC!* should be a valid password") # min length
        self.assertTrue(self.checker.check_password("test", "1234AbCd!*"), "1234AbCd!* should be a valid password")  # nominal length
        self.assertTrue(self.checker.check_password("test", "123ABCd!*"), "123ABCd!* should be a valid password")  # min lowercase
        self.assertTrue(self.checker.check_password("test", "123abcD!*"), "123abcD!* should be a valid password")  # min uppercase
        self.assertTrue(self.checker.check_password("test", "1AbCdEf!*"),"1AbCdEf!* should be a valid password") # min digit
        self.assertTrue(self.checker.check_password("test", "1AbCdEf!"), "1AbCdEf! should be a valid password")  # min special char

        self.assertFalse(self.checker.check_password("123AbC!*", "123AbC!*"),"Should not allow password that matches username" )
        self.assertFalse(self.checker.check_password("test", "Welcome2015!"), "Should not allow weak password")



