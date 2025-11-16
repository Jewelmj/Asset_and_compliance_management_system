from abc import ABC, abstractmethod
import uuid

class User(ABC):
    """
    Base User class for the system.
    Represents a person using the asset/jobsite management system.
    """

    def __init__(self, name: str, email: str):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = self.__class__.__name__

    @abstractmethod
    def get_permissions(self):
        """
        Should return a list of permissions available to the user.
        Must be implemented by child classes.
        """
        pass

    def __str__(self):
        return f"{self.role}(ID={self.user_id}, Name={self.name}, Email={self.email})"


class Admin(User):
    """
    Admin has full system-access.
    """

    def get_permissions(self):
        return [
            "manage_users",
            "manage_assets",
            "view_documents",
            "edit_documents",
            "manage_jobsites",
            "generate_qr",
        ]


class Manager(User):
    """
    Manager can manage job sites, assets, and people.
    """

    def get_permissions(self):
        return [
            "assign_assets",
            "assign_people",
            "move_assets",
            "view_documents",
            "manage_jobsites",
        ]


class Worker(User):
    """
    Worker can scan QR codes and check/move assets.
    """

    def get_permissions(self):
        return [
            "scan_qr",
            "check_asset",
            "move_asset",
            "view_assigned_assets",
            "view_jobsite",
        ]
