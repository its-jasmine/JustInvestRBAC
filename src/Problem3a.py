'''
Author: Jasmine Gad El Hak
Exercise: 3 (a)

Description:
Design and implement a simple user interface that enables a user to enter a username and chosen password,
as well as any other information that may be required. Ensure that the interface only asks for information that is
necessary for user authentication and access control.




'''
from Problem1 import *
from Problem2 import *
from Problem3b import *

import json



class UserRoleFileManager:
    def __init__(self, user_role_file):
        '''
        Initializes the PasswordFileManager and ensures the password file exists.
        :param user_role_file: Path to the file containing all the username and respective roles.

        The contents of the file is of the form: username,role

        Example:
        johndoe,Client
        billy123,Financial Advisor
        '''

        self.user_role_file = user_role_file
        self.ensure_user_role_file()

    def ensure_user_role_file(self):
        """Ensure the password file exists. Creates one if not."""
        if not os.path.exists(self.user_role_file):
            with open(self.user_role_file, 'w'):
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


    def add_new_user_record(self, username, role):
        """
        Adds a new user record to the password file.
        :param username: Username for the new user.
        :param role: Role for the new user.
        :return: True if the user record was added successfully, False if the username already exists.
        """
        self.ensure_user_role_file() # Ensure the file exists before adding
        if self.username_already_in_file(username):
            return False

        # Saves the user's record to a password file.
        with open(self.user_role_file, 'a') as file:
            file.write(
                f"{username},{role.value}\n")
        print(f"User {username} added to user role file successfully.")
        return True

    def update_user_role(self): #TODO nice to have, not explictly required by assignment description
        pass

    def retrieve_user_record(self, username):
        """
        Retrieves a user's record from the user roles file.
        :param username: Username to retrieve.
        :return: A dictionary containing the user's data:
                 - "username" (str): The username.
                 - "found" (bool): Whether the user was found.
                 - "role" (str): The user's role (if found).
        """
        self.ensure_user_role_file()  # Ensure the file exists before retreiving

        # Loads a user's record from the password file.
        with open(self.user_role_file, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == username:
                    role = data[1]
                    return {"username": username, "found": True, "role": role}
        return {"username": username, "found": False}

class EnrolUserInterface:
    def __init__(self, rbac_system,
                 password_file_manager,
                 password_checker,
                 user_role_file_manager):
        self.rbac_system = rbac_system
        self.password_file_manager = password_file_manager
        self.password_checker = password_checker
        self.user_role_file_manager = user_role_file_manager

    def run(self):
        EnrolUserInterface.print_welcome_message()
        result = self.prompt_user_for_enrollment()
        self.enroll_user(result["username"], result["password"], result["role"])


    def enroll_user(self, username, password, role):
        """Creates a new user and saves to the file."""
        pwd_file_updated = self.password_file_manager.add_new_user_record(username,password)
        if pwd_file_updated:
            self.user_role_file_manager.add_new_user_record(username, role)
            return True
        else:
            return False

    @staticmethod
    def print_welcome_message():
        """Prints a welcome message to the console."""
        print("=" * 50)
        print(" Welcome to the JustInvest User Enrollment System! ")
        print("=" * 50)
        print("This system allows you to enroll new users by providing a username, password and role")
        print("=" * 50)
        print()

    def prompt_user_for_enrollment(self):
        validInput = False
        while not validInput:
            username = input("Enter a username: ")
            if not self.password_file_manager.username_already_in_file(username):
                validInput = True

        validInput = False
        while not validInput:
            password = input("Enter a password: ")
            validInput = self.password_checker.check_password(username, password)

        validInput = False
        print("Please select a role from the following options:")
        prompt = ""
        roles = list(self.rbac_system.Role)
        for i in range(len(roles)):

            prompt += str(i) + ") " + str(roles[i].value) + "\n"
        prompt += "Enter your selection here: "

        while not validInput:
            role_index = input(prompt)
            try:
                role_index = int(role_index) # try to cast to an int
                role = roles[role_index] # try to index list of roles
                validInput = True
            except (ValueError, IndexError):
                print("\nInvalid choice. Please enter a valid number:")

        return {"username": username, "password": password, "role": role}

    def initialize_users_from_json(self, file_path):
        """Reads a JSON file and enrolls users into the system."""
        try:
            with open(file_path, mode='r') as file:
                data = json.load(file)
                for user in data["users"]:
                    if "username" in user and "password" in user:
                        self.enroll_user(user["username"], user["password"], self.rbac_system.Role(user["role"]))
                    else:
                        print(f"Invalid user data: {user}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}.")
        except Exception as e:
            print(f"An error occurred: {e}")











