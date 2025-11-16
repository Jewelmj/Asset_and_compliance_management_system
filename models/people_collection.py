class PeopleCollection:
    """
    A manager for storing and organizing users inside a place/jobsite.
    """

    def __init__(self):
        self.people = []

    def add(self, user):
        if user not in self.people:
            self.people.append(user)

    def remove(self, user):
        if user in self.people:
            self.people.remove(user)

    def list(self):
        return self.people

    def count(self):
        return len(self.people)

    def find_by_role(self, role):
        return [p for p in self.people if p.role == role]