'''
Author: Jasmine Gad El Hak
Exercise: 1 (c)

Description:
Test your implimentation.
'''

import unittest
from Problem1 import *


class TestAccessControlMechanism(unittest.TestCase):
    '''
    This test class verifies the access control mechanism initialized properly using a config file defined roles and
    operations. The roles_and_operation.json file configures the access control according to the assignment specifications.
    '''
    def setUp(self):
        """Set up the test environment by ..."""
        self.system = RoleBasedAccessControl('roles_and_operations.json')

    def tearDown(self):
        """Clean up after tests."""
        pass

    def test_load_roles(self):
        # Test the type of Role is EnumMeta
        self.assertIsInstance(self.system.Role, type(Enum), "Role should be an instance of Enum.")

        # Test total number of roles
        self.assertTrue(len(self.system.Role) == 6, "Role enum should have exactly 6 members.")

        expected_roles = {
            "CLIENT": "Client",
            "PREMIUM_CLIENT": "Premium Client",
            "FINANCIAL_ADVISOR": "Financial Advisor",
            "FINANCIAL_PLANNER": "Financial Planner",
            "EMPLOYEE": "Employee",
            "TELLER": "Teller"
        }
        for key, val in expected_roles.items():
            # Test all expected roles are present
            self.assertIn(key, self.system.Role.__members__, f"Role {key} is missing in the Role enum.")

            # Test role values are correctly assigned
            self.assertEqual(self.system.Role[key].value, val, f"Role {key} does not map correctly to its value.")

    def test_load_operations(self): # TODO update me once per user / all user operation change is made
        # Test the type of Operation is EnumMeta
        self.assertIsInstance(self.system.Operation, type(Enum), "Operation should be an instance of Enum.")

        # Test total number of roles
        self.assertTrue(len(self.system.Operation) == 7, "Role enum should have exactly 7 members.")

        # Test all expected roles are present
        expected_operations = [
            {"name": "VIEW_ACCOUNT_BALANCE", "description": "View Account Balance",
             "roles": ["Client", "Premium Client", "Employee"]},
            {"name": "VIEW_INVESTMENT_PORTFOLIO", "description": "View Investment Portfolio",
             "roles": ["Client", "Premium Client", "Employee"]},
            {"name": "MODIFY_INVESTMENT_PORTFOLIO", "description": "Modify Investment Portfolio",
             "roles": ["Premium Client", "Financial Advisor", "Financial Planner"]},
            {"name": "VIEW_FINANCIAL_ADVISOR_CONTACT_INFO", "description": "View Financial Advisor Contact Info",
             "roles": ["Client"]},
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
                                 self.system.Operation.VIEW_FINANCIAL_PLANNER_CONTACT_INFO]
        for operation in authorized_operations:
            self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.PREMIUM_CLIENT,operation))

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations):  # Unauthorized Operations
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.PREMIUM_CLIENT, operation))

    def test_role_authorized_to_perform_financial_advisor(self): # TODO fix me
        """Testing operations performed by FINANCIAL_ADVISOR"""
        authorized_operations = [self.system.Operation.VIEW_INVESTMENT_PORTFOLIO,
                                 self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO]
        for operation in authorized_operations:
            self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.PREMIUM_CLIENT,operation))

        all_operations = self.system.Operation.__members__.values()
        for operation in all_operations:
            if not (operation in authorized_operations):  # Unauthorized Operations
                self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.PREMIUM_CLIENT, operation), operation.value['description'])

    def test_role_authorized_to_perform_financial_planner(self): # TODO refactor me
        # Testing for operations where FINANCIAL_PLANNER can perform
        self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_PLANNER,
                                                               self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO))
        self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_PLANNER,
                                                               self.system.Operation.VIEW_MONEY_MARKET_INSTRUMENT))
        self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.FINANCIAL_PLANNER,
                                                                self.system.Operation.VIEW_FINANCIAL_ADVISOR_CONTACT_INFO))

    def test_role_authorized_to_perform_employee(self): # TODO refactor me
        # Testing for operations where EMPLOYEE can perform
        self.assertTrue(self.system.role_authorized_to_perform(self.system.Role.EMPLOYEE,
                                                               self.system.Operation.VIEW_ACCOUNT_BALANCE))
        self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.EMPLOYEE,
                                                                self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO))

    def test_role_authorized_to_perform_teller(self): # TODO refactor me
        # Testing for operations where TELLER can perform (Assuming TELLER doesn't have any operations)
        self.assertFalse(
            self.system.role_authorized_to_perform(self.system.Role.TELLER, self.system.Operation.VIEW_ACCOUNT_BALANCE))
        self.assertFalse(self.system.role_authorized_to_perform(self.system.Role.TELLER,
                                                                self.system.Operation.MODIFY_INVESTMENT_PORTFOLIO))




