import unittest
from unittest.mock import MagicMock
from system import System

class TestSystem(unittest.TestCase):
    def setUp(self):
        # Creating a mock database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = self.mock_connection.cursor()

        # Creating a System instance with the mock cursor
        self.system = System()
        self.system.cursor = self.mock_cursor

    def test_get_movie_list(self):
        # Mocking the cursor's fetchall method to return movie data
        movie_data = [('Movie 1', 'Director 1', 'Genre 1', 2022),
                      ('Movie 2', 'Director 2', 'Genre 2', 2023)]
        self.mock_cursor.fetchall.return_value = movie_data

        # Calling the get_movie_list method
        movies = self.system.get_movie_list()

        # Asserting that the returned movie list matches the expected data
        self.assertEqual(movies, movie_data)

    def test_reserve_ticket(self):
        # Mocking the cursor's execute method
        self.mock_cursor.execute.return_value = None
        
        # Calling the reserve_ticket method with ticket data
        reservation_status = self.system.reserve_ticket('Movie 1', 'JohnDoe', 3)

        # Asserting that the reservation was successful
        self.assertTrue(reservation_status)

    def test_get_user_reservations(self):
        # Mocking the cursor's fetchall method to return reservation data
        reservation_data = [('Movie 1', 'JohnDoe', 3),
                            ('Movie 2', 'JohnDoe', 2)]
        self.mock_cursor.fetchall.return_value = reservation_data

        # Calling the get_user_reservations method
        reservations = self.system.get_user_reservations('JohnDoe')

        # Asserting that the returned reservations match the expected data
        self.assertEqual(reservations, reservation_data)

if __name__ == '__main__':
    unittest.main()
