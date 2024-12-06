import unittest
from Problem4 import *
from TEST_CONSTANTS import *

class TestLoginUserInterface(unittest.TestCase):
    def setUp(self):
        """Set up the test environment by ..."""
        pswd_file_manager = PasswordFileManager(password_file=TEST_PASSWORD_FILE,
                                                hash_function=HASH_FUNCTION,
                                                hash_length=HASH_LENGTH,
                                                salt_length=SALT_LENGTH,
                                                iteration_count=ITERATION_COUNT)
        rbac = RoleBasedAccessControl(TEST_ROLES_AND_OPERATIONS_FILE)
        user_role_manager = UserRoleFileManager(TEST_USER_ROLES_FILE)
        self.login_ui = LoginUserInterace(rbac_system=rbac,
                                          pswd_file_manager=pswd_file_manager,
                                          user_roles_file_manager=user_role_manager)
        self.enrol_ui = EnrolUserInterface(rbac_system=rbac,
                                           password_file_manager=pswd_file_manager,
                                           user_role_file_manager=user_role_manager,
                                           password_checker=ProactivePasswordChecker(TEST_WEAK_PASSWORDS))

    def tearDown(self):
        """Clean up after tests."""
        os.remove(TEST_PASSWORD_FILE)
        os.remove(TEST_USER_ROLES_FILE)

    def test_user_login_success(self):
        """Test successful login."""
        username = "test"
        password = "SecurePassword123!"
        self.enrol_ui.enroll_user(username, password, self.enrol_ui.rbac_system.Role("Client"))
        result = self.login_ui.login_user(username, password)
        self.assertTrue(result, "Login should succeed with correct password.")

    def test_user_login_failure(self):
        """Test login failure with wrong password."""
        username = "test"
        password = "SecurePassword123!"
        wrong_password = "WrongPassword123!"
        self.enrol_ui.enroll_user(username, password, self.enrol_ui.rbac_system.Role("Client"))
        result = self.login_ui.login_user(username, wrong_password)
        self.assertFalse(result, "Login should fail with incorrect password.")

    def test_nonexistent_user_login(self):
        """Test login failure for nonexistent user."""
        result = self.login_ui.login_user("nonexistent_user", "SomePassword123!")
        self.assertFalse(result, "Login should fail for nonexistent user.")

