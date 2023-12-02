class Customer(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.bookings = []