# The constants for the file paths that will be used in the test classes
TEST_ROLES_AND_OPERATIONS_FILE = '../src/config/roles_and_operations.json'
TEST_PASSWORD_FILE = '../src/data/passwd_test.txt'
TEST_WEAK_PASSWORDS = '../src/config/weak_passwords.txt'
TEST_USER_ROLES_FILE = "../src/data/user_roles.txt"

SALT_LENGTH = 16  # 16 bytes = 128 bits
HASH_LENGTH = 32  # 32 bytes for SHA-256 hash
HASH_FUNCTION = 'sha256' # the hash function that will be iteratively applied
ITERATION_COUNT = 100000