'''
Author: Jasmine Gad El Hak
Exercise: 1 (c)

Description:
Implement the access control mechanism to ensure the user is only allowed to perform their authorized operations.
'''
from enum import Enum
from pathlib import Path
import json


class RoleBasedAccessControl:
    '''A Role Based Access Control System that is dynamically configured based on the provided json file containing all
    the roles and operations that will be supported by the system. The file must be of the following form:
    {
      "roles": ["RoleName1","RoleName2", ...],
      "operations": [
        {"name": "An Operation", "roles": ["RoleName1", ...]},
        ...
      ]
    }
    '''
    def __init__(self, file_path):
        self.Role, self.Operation = RoleBasedAccessControl.load_roles_operations(file_path)

    def role_authorized_to_perform(self, role: Enum, operation: Enum):
        '''
        Checks if the given role is allowed to perform this operation.
        :param role: The role of the user attempting to perform operation.
        :param operation: The operation that the user is attempting to perform.
        :return: True if provided role is authorized to perform the given operation, otherwise False
        '''
        if not (isinstance(role, self.Role)):
            raise Exception("Must provide a Role enum value")
        if not (isinstance(operation, self.Operation)):
            raise Exception("Must provide an Operation enum value")

        return role in operation.value['authorized_roles']

    #### Helper Functions ####
    @staticmethod
    def create_enum(name, items):
        """Dynamically creates an Enum."""
        return Enum(name, {item.replace(" ", "_").upper(): item for item in items})

    @staticmethod
    def load_roles_operations(file_path):
        '''
        Loads Roles and Operations from JSON
        :param: file_path: the file path of the JSON containing the desired roles and operations
        :return: tuple containing the Role and Operation enums, constructed based on the given config data.
        '''
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File {file_path} not found.")

        with open(file_path, "r") as f:
            data = json.load(f)

        if not ("roles" in data):
            raise Exception("Cannot configure roles: 'roles' key not found. ")

        # populate Role enum
        Role = RoleBasedAccessControl.create_enum("Role", data["roles"])

        if not ("operations" in data):
            raise Exception("Cannot configure roles: 'operations' key not found. ")

        # populate Operation enum
        operations = {}
        for operation_data in data["operations"]:
            name = operation_data["name"].upper().replace(" ", "_")
            description = operation_data["name"]
            authorized_roles = {Role[role.replace(" ", "_").upper()] for role in operation_data["roles"]}
            operations[name] = {'description': description, 'authorized_roles': authorized_roles}
        Operation = Enum("Operation", operations)

        return (Role, Operation)

if __name__ == "__main__":
    RoleBasedAccessControl('roles_and_operations.json')
