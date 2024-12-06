'''
Author: Jasmine Gad El Hak
Exercise: 1 (c)

Description:
Test your implimentation.
'''

import unittest
from Problem1 import *
from TEST_CONSTANTS import TEST_ROLES_AND_OPERATIONS_FILE

class TestAccessControlMechanism(unittest.TestCase):
    '''
    This test class verifies the access control mechanism initialized properly using a config file defined roles and
    operations. The roles_and_operation.json file configures the access control according to the assignment specifications.
    '''
    def setUp(self):
        """Set up the test environment by ..."""
        self.system = RoleBasedAccessControl(TEST_ROLES_AND_OPERATIONS_FILE)

    def tearDown(self):
        """Clean up after tests."""
        pass

    def test_load_roles(self):
        # Test the type of Role is EnumMeta
        self.assertIsInstance(self.system.Role, type(Enum), "Role should be an instance of Enum.")

        # Test total number of roles
        self.assertEqual(len(self.system.Role), 5, "Role enum should have exactly 5 members.")

        expected_roles = {
            "CLIENT": "Client",
            "PREMIUM_CLIENT": "Premium Client",
            "FINANCIAL_ADVISOR": "Financial Advisor",
            "FINANCIAL_PLANNER": "Financial Planner",
            "TELLER": "Teller"
        }
        for key, val in expected_roles.items():
            # Test all expected roles are present
            self.assertIn(key, self.system.Role.__members__, f"Role {key} is missing in the Role enum.")

            # Test role values are correctly assigned
            self.assertEqual(self.system.Role[key].value, val, f"Role {key} does not map correctly to its value.")

    def test_load_operations(self):
        # Test the type of Operation is EnumMeta
        self.assertIsInstance(self.system.Operation, type(Enum), "Operation should be an instance of Enum.")

        # Test total number of roles
        self.assertEqual(len(self.system.Operation), 7, "Role enum should have exactly 7 members.")

        # Test all expected roles are present
        expected_operations = [
            {"name": "VIEW_ACCOUNT_BALANCE", "description": "View Account Balance",
             "roles": ["Client", "Premium Client","Financial Advisor", "Financial Planner","Teller"]},
            {"name": "VIEW_INVESTMENT_PORTFOLIO", "description": "View Investment Portfolio",
             "roles": ["Client", "Premium Client", "Financial Advisor", "Financial Planner","Teller"]},
            {"name": "MODIFY_INVESTMENT_PORTFOLIO", "description": "Modify Investment Portfolio",
             "roles": ["Premium Client", "Financial Advisor", "Financial Planner"]},
            {"name": "VIEW_FINANCIAL_ADVISOR_CONTACT_INFO", "description": "View Financial Advisor Contact Info",
             "roles": ["Client", "Premium Client" ]},
            {"name": "VIEW_FINANCIAL_PLANNER_CONTACT_INFO", "description": "View Financial Planner Contact Info",
             "roles": ["Premium Client"]},
            {"name": "VIEW_MONEY_MARKET_INSTRUMENT", "description": "View Money Market Instrument",
             "roles": ["Financial Planner"]},
            {"name": "VIEW_PRIVATE_CONSUMER_INSTRUMENT", "description": "View Private Consumer Instrument",
             "roles": ["Financial Advisor", "Financial Planner"]}
        ]

        for operation in expected_operations:
            self.assertIn(operation['name'], self.system.Operation.__members__,
                          f"Operation {operation['name']} is missing in the Operation enum.")

            # Verify the attributes of the operation
            enum_operation = self.system.Operation[operation['name']]
            self.assertEqual(enum_operation.value['description'], operation['description'],
                             f"Description mismatch for {operation['name']}.")
            self.assertEqual(set(role.value for role in enum_operation.value['authorized_roles']),
                             set(operation['roles']), f"Roles mismatch for {operation['name']}.")
    def test_load_time_restrictions(self):
        # Test total number of roles with time restrictions
        self.assertTrue(isinstance(self.system.timeRestrictions, dict), "Time restrictions should be a dictionary")
        time_restricted_roles = self.system.timeRestrictions.keys()
        self.assertEquals(len(time_restricted_roles), 1, "Only 1 role should have time restrictions.")
        self.assertTrue(self.system.Role.TELLER in time_restricted_roles, "Teller should have time restrictions")

        # Verify time restriction data for Teller
        time_restriction_data = self.system.timeRestrictions[self.system.Role.TELLER]
        self.assertTrue(isinstance(time_restriction_data, dict), "Time restriction for a particular role should be a dictionary")
        self.assertEquals(len(time_restriction_data.keys()), 2, "Time restriction data should have two values")
        self.assertTrue("start" in time_restriction_data.keys(), "Time restriction data should have start value")
        self.assertTrue("end" in time_restriction_data.keys(), "Time restriction data should have end value")

        self.assertEquals(time_restriction_data["start"], 9, "Teller start should be 9 ")
        self.assertEquals(time_restriction_data["end"], 17, "Teller end should be 17 (i.e., 5 pm)")

    def test_role_authorized_to_perform_client(self):
        """Testing operations performed by CLIENT"""
        authorized_operations = [self.system.Operation.VIEW_ACCOUNT_BALANCE,
                                 self.system.Operation.VIEW_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.VIEW_FINANCIAL_ADVISOR_CONTACT_INFO]

        for operation in authorized_operations:
            self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.CLIENT,operation))


        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations): # Unauthorized Operations
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.CLIENT,operation))

    def test_role_authorized_to_perform_premium_client(self):
        """Testing operations performed by PREMIUM_CLIENT"""
        authorized_operations = [self.system.Operation.VIEW_ACCOUNT_BALANCE,
                                 self.system.Operation.VIEW_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.VIEW_FINANCIAL_ADVISOR_CONTACT_INFO,
                                 self.system.Operation.VIEW_FINANCIAL_PLANNER_CONTACT_INFO]
        for operation in authorized_operations:
            self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.PREMIUM_CLIENT,operation))

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations):  # Unauthorized Operations
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.PREMIUM_CLIENT, operation))

    def test_role_authorized_to_perform_financial_advisor(self): # TODO fix me
        """Testing operations performed by FINANCIAL_ADVISOR"""
        authorized_operations = [self.system.Operation.VIEW_ACCOUNT_BALANCE,
                                 self.system.Operation.VIEW_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.VIEW_PRIVATE_CONSUMER_INSTRUMENT]
        for operation in authorized_operations:
            self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_ADVISOR,operation))

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations):  # Unauthorized Operations
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_ADVISOR, operation), operation.value['description'])

    def test_role_authorized_to_perform_financial_planner(self):
        """Testing operations performed by FINANCIAL_PLANNER"""
        authorized_operations = [self.system.Operation.VIEW_ACCOUNT_BALANCE,
                                 self.system.Operation.VIEW_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.VIEW_MONEY_MARKET_INSTRUMENT,
                                 self.system.Operation.VIEW_PRIVATE_CONSUMER_INSTRUMENT]
        for operation in authorized_operations:
            self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_PLANNER, operation))

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations):  # Unauthorized Operations
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_PLANNER, operation),
                                 operation.value['description'])

    def test_role_authorized_to_perform_teller_authorized_hours(self):
        """Testing operations performed by TELLER during authorized hours"""
        authorized_operations = [self.system.Operation.VIEW_ACCOUNT_BALANCE,
                                 self.system.Operation.VIEW_INVESTMENT_PORTFOLIO]

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        # Some edge and nominal cases for authorized times
        authorized_times = [datetime.datetime(year, month, day, hour=9, minute=0), # 9 AM
                            datetime.datetime(year, month, day, hour=12, minute=0), # 12 PM
                            datetime.datetime(year, month, day, hour=16, minute=59)] # 4:49 PM

        for operation in authorized_operations:
            for time in authorized_times:
                self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.TELLER, operation, time), f"Teller should be authorized to perform {operation.value['description']} during authorized hours ")

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations):  # Unauthorized Operations
                for time in authorized_times:
                    self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.TELLER, operation, time),
                                     operation.value['description'])

    def test_role_authorized_to_perform_teller_unauthorized_hours(self):
        """Testing operations performed by TELLER during unauthorized hours"""
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        # Some test cases for unauthorized times
        unauthorized_times = [datetime.datetime(year, month, day, hour=1, minute=0), # 1 AM
                              datetime.datetime(year, month, day, hour=8, minute=59), # 8:59 AM
                              datetime.datetime(year, month, day, hour=17, minute=1), # 5:01 AM
                              datetime.datetime(year, month, day, hour=22, minute=0)] # 10 PM

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            for time in unauthorized_times:
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.TELLER, operation, time),
                             operation.value['description'])

