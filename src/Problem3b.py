'''
Author: Jasmine Gad El Hak
Exercise: 3 (b)

Description:
Design and implement the proactive password checker.
Design and implement the proactive password checker to be used when a user enrols in the system.

The prototype must implement a proactive password checker
that ensures that all passwords adhere to the following password policy:
• Passwords must be between 8 and 12 characters in length.
• Passwords must include at least:
– one upper-case letter
– one lower-case letter
– one numerical digit
– one special character from the following: !, @, #, $, %, *, &
• Passwords found on a list of common weak passwords must be prohibited. Note that the list should be flexible to allow for the addition of new exclusions over time.
• Passwords matching the username must be prohibited.
'''

# Default values
WEAK_PASSWORDS_FILE = 'config/weak_passwords.txt'

class ProactivePasswordChecker:
    def __init__(self, weak_passwords_file=WEAK_PASSWORDS_FILE):
        with open(weak_passwords_file, 'r') as file:
            self.weak_passwords = [weak_password.rstrip() for weak_password in file]

    def check_password(self, username, password):
        if self.weak_passwords == []:
            print("Weak passwords file has not been configured!")
            return False

        min_length = 8
        max_length = 12

        valid_length = min_length <= len(password) <= max_length
        has_lowercase = any(char.islower() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special_char = any(char in '!@#$%*&' for char in password)

        weak = password in self.weak_passwords
        matches_username = username == password

        if (valid_length and has_uppercase and has_lowercase and has_digit and has_special_char and not weak and not matches_username): return True

        print("The password you have chosen does not adhere to the password policy.")

        if not valid_length:
            print("- Must be between 8 and 12 characters in length")
        if not has_lowercase:
            print("- Include at least one lower case letter")
        if not has_uppercase:
            print("- Include at least one upper case letter")
        if not has_digit:
            print("- Include at least one number")
        if not has_special_char:
            print("- Include at least one special character (!, @, #, $, %, *, &)")
        if weak:
            print("- Password is too common")
        if matches_username:
            print("- Must not be identical to username")

        return False

