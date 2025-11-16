from models.user import User

class UserService:
    def create_user(self, name, email, role):
        user = User(name, email, role)
        return user