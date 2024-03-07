import unittest
from unittest.mock import MagicMock
from system import System
from user import Customer, Admin

class TestSystem(unittest.TestCase):

    def setUp(self):
        # Initialize your System object
        self.system = System(database="cinema.db")

    def test_login_success(self):
        # Mocking the database connection and cursor
        self.system.connection = MagicMock()
        self.system.cursor = MagicMock()

        # Mocking the execute method to return user data with correct credentials
        user_data = (2, "Thy", "Khuu", "bachthy94@gmail.com", "bachthy20fc", "Yes")
        self.system.cursor.fetchone.return_value = user_data

        # Testing the login method with correct credentials
        user, role = self.system.login("bachthy94@gmail.com", "bachthy20fc")

        # Assert that user and role are not None
        self.assertIsNotNone(user)
        self.assertIsNotNone(role)
        self.assertIsInstance(user, Customer)
        self.assertEqual(user.email, "bachthy94@gmail.com")
        self.assertEqual(role, "customer")

    def test_login_success_admin(self):
            # Mocking the database connection and cursor
            self.system.connection = MagicMock()
            self.system.cursor = MagicMock()

            # Mocking the execute method to return user data for an admin
            self.system.cursor.fetchone.return_value = (1, "Admin", "User", "admin@admin.com", "admin", "No")

            # Testing the login method with valid admin credentials
            user, role = self.system.login("admin@admin.com", "admin")

            # Assert that user is an instance of Admin and role is 'admin'
            self.assertIsInstance(user, Admin)
            self.assertEqual(role, 'admin')
    
              
if __name__ == '__main__':
    unittest.main()
