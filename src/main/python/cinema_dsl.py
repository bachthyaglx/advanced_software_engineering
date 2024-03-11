import sqlite3

class CinemaDatabase:
    def __init__(self):
        # Initialize any necessary attributes or connections to the database
        self.connection = None

    def connect(self, database):
        # Establish connection to the database
        self.connection = sqlite3.connect(database)
        print("Connected to database:", database)
        return self  # Return self to allow method chaining

    def get_movie_with_highest_rating(self):
        # Retrieve the movie with the highest rating from the database
        query = "SELECT name FROM movies ORDER BY rate DESC LIMIT 1"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return "No movies found in the database"

# Example usage of the DSL
cinema_database = CinemaDatabase()
highest_rated_movie = cinema_database.connect("cinema.db").get_movie_with_highest_rating()
print("Movie with the highest rating:", highest_rated_movie)
