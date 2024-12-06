'''
Author: Jasmine Gad El Hak
Exercise: 2 (c):

Description:
Create the password file and implement relevant functions.
    Create a password file based on your design in (a) and (b).
    Your password file should be a text file called passwd.txt.
Implement two functions:
    1) properly add new records to the password file (when enrolling a new user)
    2) retrieve records from the password file (when a user logs in).
'''

import os
import base64
from hashlib import pbkdf2_hmac

class PasswordFileManager:
    def __init__(self, password_file:str, hash_function: str, salt_length:int, iteration_count:int, hash_length:int):
        '''
        Initializes the PasswordFileManager and ensures the password file exists.
        :param password_file: Path to the password file.
        :param hash_function: Hash function used for password hashing (e.g., 'sha256').
        :param salt_length: Length of the salt for password hashing.
        :param iteration_count: Number of iterations for PBKDF2-HMAC.
        :param hash_length: Length of the generated password hash.
        '''

        self.password_file = password_file
        self.ensure_password_file()

        self.hash_function = hash_function
        self.salt_length = salt_length
        self.iteration_count = iteration_count
        self.hash_length = hash_length

    def ensure_password_file(self):
        """Ensure the password file exists. Creates one if not."""
        if not os.path.exists(self.password_file):
            with open(self.password_file, 'w'):
                pass  # Create an empty file if it doesn't exist

    def username_already_in_file(self, username):
        '''
        Determines whether username is already saved in the password file.
        :param username: username to search for in the password file.
        :return: True if username is already in password file, otherwise False
        '''
        if self.retrieve_user_record(username)["found"]:
            print("Username is already in use!")
            return True
        return False

    def hash_password(self, password, salt):
        """
        Hashes the given password with PBKDF2-HMAC and the provided salt.
        :param password: Plaintext password to hash.
        :param salt: Salt for the hashing process.
        :return: The derived password hash.
        """
        return pbkdf2_hmac(self.hash_function, password.encode('utf-8'), salt, self.iteration_count)

    def add_new_user_record(self, username, password):
        """
        Adds a new user record to the password file.
        :param username: Username for the new user.
        :param password: Plaintext password for the new user.
        :return: True if the user record was added successfully, False if the username already exists.
        """
        self.ensure_password_file() # Ensure the file exists before adding
        if self.username_already_in_file(username):
            return False

        # Generate salt and hash the password
        salt = os.urandom(self.salt_length)
        hash = self.hash_password(password, salt)

        # Saves the user's record to a password file.
        with open(self.password_file, 'a') as file:
            file.write(
                f"{username},{base64.b64encode(salt).decode('utf-8')},{base64.b64encode(hash).decode('utf-8')}\n")
        print(f"User {username} added to password file successfully.")
        return True

    def retrieve_user_record(self, username):
        """
        Retrieves a user's record from the password file.
        :param username: Username to retrieve.
        :return: A dictionary containing the user's data:
                 - "username" (str): The username.
                 - "found" (bool): Whether the user was found.
                 - "salt" (bytes): The user's salt (if found).
                 - "hash" (bytes): The user's password hash (if found).
        """
        self.ensure_password_file()  # Ensure the file exists before retreiving

        # Loads a user's record from the password file.
        with open(self.password_file, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == username:
                    salt = base64.b64decode(data[1])
                    hash = base64.b64decode(data[2])
                    return {"username": username, "found": True, "salt": salt, "hash" : hash}
        return {"username": username, "found": False}







