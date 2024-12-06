from Problem3a import *

class LoginUserInterace:
    def __init__(self, rbac_system:RoleBasedAccessControl,pswd_file_manager:PasswordFileManager, user_roles_file_manager:UserRoleFileManager):
        self.logged_in_username = None
        self.logged_in_user_role = None
        self.rbac_system = rbac_system
        self.Role = self.rbac_system.Role
        self.pswd_file_manager = pswd_file_manager
        self.user_roles_file_manager = user_roles_file_manager

    def run(self):
        LoginUserInterace.print_welcome_message()
        logged_in = False
        while not logged_in:
            username, password = LoginUserInterace.prompt_user_for_credentials()
            logged_in = self.login_user(username, password)

        op = "_"
        while True:
            op = self.prompt_for_operations()
            if op == "Q": break
            if self.rbac_system.role_authorized_to_perform(self.logged_in_user_role, op):
                print(self.logged_in_username + " successfully performed operation " + op.value["description"])
            else:
                print(f"UNAUTHORIZED OPERATION: {self.logged_in_username} does not have the permissions to perform this operation")
            print()
        print("Thanks for using JustInvest, have a great day!")


    def login_user(self, username, password):
        """Verifies user credentials by checking the stored password hash."""
        data = self.pswd_file_manager.retrieve_user_record(username)
        if data["found"]:
            salt = data["salt"]
            hash = data["hash"]

            role_data = self.user_roles_file_manager.retrieve_user_record(username)
            if role_data["found"]:
                user_role = self.Role(self.user_roles_file_manager.retrieve_user_record(username)["role"])
            else:
                raise Exception(f"{username} was found in password file but not in the user roles file!")

            if self.verify_password(password, salt, hash):
                    print(f"{username} logged in successfully.")
                    print()
                    self.logged_in_username = username
                    self.logged_in_user_role = user_role
                    return True
        print(f"Incorrect credentials, please try again.")
        print()
        return False

    @staticmethod
    def print_welcome_message():
        """Prints a welcome message to the console."""
        print("=" * 50)
        print(" Welcome to the JustInvest Login System! ")
        print("=" * 50)
        print("This system allows enrolled users to login by providing their correct username and password.")
        print("Once login is successful, the system will display access permissions for the operations of the system!")
        print("=" * 50)
        print("Let's get started!")
        print()

    @staticmethod
    def prompt_user_for_credentials():
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        return (username,password)

    def verify_password(self, password, salt, hash): # TODO not working during manual testing
        """Verifies the password by comparing the hash."""
        return self.pswd_file_manager.hash_password(password, salt) == hash

    def prompt_for_operations(self):
        print("Please select an operation to perform:")
        prompt = ""
        operations = list(self.rbac_system.Operation)
        for i in range(len(operations)):
            prompt += str(i) + ") " + str(operations[i].value["description"]) + "\n"
        prompt += "Q - Quit\n"
        prompt += "Enter your selection here: "
        validInput = False
        while not validInput:
            op_index = input(prompt)
            if op_index == "Q": return "Q"
            try:
                op_index = int(op_index)  # try to cast to an int
                op = operations[op_index]  # try to index list of roles
                validInput = True
            except (ValueError, IndexError):
                print("\nInvalid choice. Please enter a valid number:")

        return op

if __name__ == "__main__":
    LoginUserInterace().run()




