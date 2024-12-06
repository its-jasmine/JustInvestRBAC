'''
Author: Jasmine Gad El Hak
Exercise: 2 (d):

Description:
Test the password file usage.
'''

import unittest
from Problem2 import *
from TEST_CONSTANTS import TEST_PASSWORD_FILE, HASH_FUNCTION, HASH_LENGTH, SALT_LENGTH, ITERATION_COUNT



class TestPasswordFileManager(unittest.TestCase):
    def setUp(self):
        """Set up the test environment by cleaning up any old password files.""" # TODO make sure all tests cleanup their files properly
        if os.path.exists(TEST_PASSWORD_FILE):
            os.remove(TEST_PASSWORD_FILE)  # Ensure no leftover data

        self.pswd_file_manager = PasswordFileManager(password_file=TEST_PASSWORD_FILE,
                                                     hash_function=HASH_FUNCTION,
                                                     hash_length=HASH_LENGTH,
                                                     salt_length=SALT_LENGTH,
                                                     iteration_count=ITERATION_COUNT)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.pswd_file_manager.password_file):
            os.remove(self.pswd_file_manager.password_file)

    def test_ensure_password_file(self):
        """
        Test that the password file is created if it does not exist.
        """
        self.assertTrue(os.path.exists(self.pswd_file_manager.password_file), "Password file was not created.")

    def test_add_new_user_record(self):
        """Test if user records can be added correctly."""
        username = "test"
        password = "SecurePassword123!"

        initial_file_length = 0 # file should be intially empty

        result = self.pswd_file_manager.add_new_user_record(username, password)
        self.assertTrue(result, "Failed to add new user record.")

        with open(self.pswd_file_manager.password_file, "r") as file:
            lines = file.readlines()

        # Verify the new line was added
        self.assertEqual(len(lines), initial_file_length + 1,
                         "File length should increase by 1 after adding user.")

        data = lines[0].strip().split(',')
        self.assertTrue(len(data) == 3) # should contain 3 values (username, salt, hash)
        self.assertTrue(data[0] == username)
        self.assertTrue(data[2] == base64.b64encode(self.pswd_file_manager.hash_password(password, base64.b64decode(data[1]))).decode('utf-8'))

    def test_duplicate_user(self):
        """
        Test that duplicate usernames cannot be added.
        """
        username = "duplicate_user"
        password = "Password1!"
        self.pswd_file_manager.add_new_user_record(username, password)

        initial_file_length = 1 # file should be intially have one user
        result = self.pswd_file_manager.add_new_user_record(username, password)

        self.assertFalse(result, "Duplicate username was added.")
        with open(self.pswd_file_manager.password_file, 'r') as file:
            content = file.readlines()
        self.assertEqual(len(content), initial_file_length, "Password file contains duplicate records.")


    def test_user_record_retrieval(self):
        """Test if user records can be retrieved correctly."""
        username = "test"
        password = "SecurePassword123!"
        self.pswd_file_manager.add_new_user_record(username, password)

        result = self.pswd_file_manager.retrieve_user_record(username)
        self.assertTrue(result['found'], "User should be found in the password file.")
        self.assertEqual(result['username'], username, "Username should match.")
        self.assertTrue(self.pswd_file_manager.hash_password(password, result['salt']) == result['hash'], "Password hashed with salt should match hash returned.")

    def test_retrieve_nonexistent_user(self):
        """
        Test retrieving a user record that does not exist.
        """
        username = "nonexistent_user"
        record = self.pswd_file_manager.retrieve_user_record(username)

        self.assertFalse(record["found"], "Nonexistent user was incorrectly found.")
        self.assertEqual(record["username"], username, "Username does not match the queried username.")

    def test_hash_password_consistency(self):
        """
        Test that the password hash is consistent for the same input.
        """
        password = "ConsistentPass123!"
        salt = os.urandom(16)
        hash1 = self.pswd_file_manager.hash_password(password, salt)
        hash2 = self.pswd_file_manager.hash_password(password, salt)

        self.assertEqual(hash1, hash2, "Password hash is not consistent for the same input.")

    def test_hash_password_uniqueness(self):
        """
        Test that the password hash is unique for different passwords.
        """
        password1 = "UniquePass123!"
        password2 = "DifferentPass456!"
        salt = os.urandom(self.pswd_file_manager.salt_length)
        hash1 = self.pswd_file_manager.hash_password(password1, salt)
        hash2 = self.pswd_file_manager.hash_password(password2, salt)

        self.assertNotEqual(hash1, hash2, "Password hashes are not unique for different inputs.")

    def test_hash_password_uniqueness_same_pass(self):
        """
        Test that the password hash is unique for same password with different salts.
        """
        password = "PopularPass123!"
        salt1 = os.urandom(self.pswd_file_manager.salt_length)
        salt2 = os.urandom(self.pswd_file_manager.salt_length)
        self.assertNotEqual(salt1,salt2)
        hash1 = self.pswd_file_manager.hash_password(password, salt1)
        hash2 = self.pswd_file_manager.hash_password(password, salt2)
        self.assertNotEqual(salt1, salt2)

        self.assertNotEqual(hash1, hash2, "Password hashes are not unique for different salts.")

    def test_file_integrity_after_operations(self):
        """
        Test that the file contents remain consistent after multiple operations.
        """
        users = [("user1", "Pass1!"), ("user2", "Pass2!"), ("user3", "Pass3!")]
        for username, password in users:
            self.pswd_file_manager.add_new_user_record(username, password)

        with open(self.pswd_file_manager.password_file, 'r') as file:
            lines = file.readlines()

        self.assertEqual(len(lines), len(users), "File contains incorrect number of records.")
        for username, _ in users:
            self.assertTrue(any(username in line for line in lines), f"Username {username} not found in file.")

if __name__ == "__main__":
    unittest.main()
