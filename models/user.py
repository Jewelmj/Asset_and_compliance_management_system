import uuid

class User:
    """
    Pure data model representing a system user.
    No permission or role logic here.
    """

    def __init__(self, name: str, email: str, role: str):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role   # "Admin", "Manager", "Worker"

    def __str__(self):
        return f"{self.role}(ID={self.user_id}, Name={self.name}, Email={self.email})"