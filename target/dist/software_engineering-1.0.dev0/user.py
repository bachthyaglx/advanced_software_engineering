# user.py
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Customer(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.bookings = []

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
