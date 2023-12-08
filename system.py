# system.py
import sqlite3
import datetime
from user import User, Customer, Admin
from movie import Movie

class System:
    def __init__(self, database="cinema.db"):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.customers = []  # List to store customer objects

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email=? AND password=?"
        self.cursor.execute(query, (email, password))
        user_data = self.cursor.fetchone()

        if user_data:
            if user_data[5]=='No':
                return Admin(email, password), 'admin'  
            else:  
                return Customer(email,password), 'customer'
        else:
            print('User not existed! Please register an account!')
            return None, None

    def register_customer(self, firstname, lastname, email, password):
        insert_query = """INSERT INTO users (firstname, lastname, email, password) VALUES (?,?,?,?)"""
        self.cursor.execute(insert_query, (firstname, lastname, email, password))
        self.connection.commit()
        
        return Customer(email, password)

    def run(self):
        print("\nWelcome to our Cinema! Latest movies:\n")
        self.fetch_movies()
        
        while True:
            print(f"\n{'1. Login':<15}{'2. Register':<18}{'3. Exit'}")
            choice = input("\nSelect an option: ")
        
            if choice == "1":
                email = input("\nEnter email: ")
                password = input("Enter password: ")
                user, role = self.login(email, password)
                if user:
                    print(f"\nWelcome, {email}! You are logged in as {role}.")
                    if role == "customer":
                        self.customer_menu(user)
                    elif role == "admin":
                        self.admin_menu(user)
                else:
                    print("\nUser not existed. Please try again or register an account!")

            elif choice == "2":
                firstname = input("\nFirstname: ")
                lastname = input("Lastname: ")
                email = input("Email: ")
                password = input("Password: ")
                new_customer = self.register_customer(firstname, lastname, email, password)
                print(f"\nAccount created for {email}. You can now log in.")

            elif choice == "3":
                print("\nGoodbye!")
                break

            else:
                print("\nInvalid choice. Please try again.")

    def customer_menu(self, customer):
        while True:
            print(f"\n{'1. View Movies and Showtimes':<15}{'2. Book a Seat':<15}{'3. Manage Bookings':<15}{'4. Logout'}")
            customer_choice = input("\nSelect an option: ")

            if customer_choice == "1":
                self.view_movies()

            elif customer_choice == "2":
                self.book_ticket(customer)

            elif customer_choice == "3":
                self.manage_bookings(customer)

            elif customer_choice == "4":
                print("\nLogging out...")
                break
            
            else:
                print("\nInvalid choice. Please try again.")

    def admin_menu(self, admin):
        while True:
            print(f"{'1. View Movies and Showtimes':<15}{'2. Manage Movies and Schedules':<15}{'3. Manage Customer Bookings':<15}{'4. Logout'}")
            admin_choice = input("\nSelect an option: ")

            if admin_choice == "1":
                self.view_movies()

            elif admin_choice == "2":
                self.manage_movies()

            elif admin_choice == "3":
                self.manage_customer_bookings()

            elif admin_choice == "4":
                print("Logging out...")
                break

            else:
                print("\nInvalid choice. Please try again.")

    def view_movies(self):
        query = "SELECT * FROM movies"
        self.cursor.execute(query)
        movies_data = self.cursor.fetchall()
        movies = [Movie(*movie_data) for movie_data in movies_data]
        
        print(f"{'-' * 70}")
        print(f"{'No':<5}{'Name':<30}{'Language':<15}{'Release':<10}")
        print(f"{'-' * 70}")
        for movie in movies:
            print(f"{movie.id:<5}{movie.name:<30}{movie.language:<15}{movie.release:<10}")
        print(f"{'-' * 70}")
            
    def book_ticket(self, customer):
        print("\nBooking a Ticket:")
        self.view_movies()

        # Get user's movie choice
        movie_id = input("\nSelect a movie (enter movie ID): ")
        try:
            movie_id = int(movie_id)
            if movie_id <= 0:
                raise ValueError("Movie ID must be a positive integer.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid positive integer for Movie ID.")
            return

        # Get user's room type choice
        print("\nAvailable Room Types:")
        print("1. 2D")
        print("2. 3D")
        room_type_choice = input("Select a room type (enter room type number): ")

        # Get available seats based on room type
        available_seats = self.get_available_seats(movie_id, room_type_choice)

        if not available_seats:
            print("No available seats for the selected room type.")
            return

        # Display available seats
        print("\nAvailable Seats:")
        for seat in available_seats:
            print(f"Seat ID: {seat[0]}, Room Number: {seat[1]}, Seat Number: {seat[2]}")

        # Get user's seat choice
        seat_id = input("\nSelect a seat (enter seat ID): ")
        try:
            seat_id = int(seat_id)
            if seat_id <= 0:
                raise ValueError("Seat ID must be a positive integer.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid positive integer for Seat ID.")
            return

        # Get the current date (you may want to use a more sophisticated method for real-world scenarios)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add ticket information to the "tickets" table
        insert_ticket_query = """INSERT INTO tickets (users_id, movies_id, room_id, seat_id, date) VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(insert_ticket_query, (customer.id, movie_id, seat[0], seat[1], current_date))
        self.connection.commit()

        print("\nTicket booked successfully!")
        
    def manage_bookings(self, customer):
        print("\nManaging Bookings:")
        while True:
            print(f"{'\n1. View Your Bookings':<15}{'2. Back to Customer Menu'}")
            customer_choice = input("Select an option: ")

            if customer_choice == "1":
                self.view_customer_bookings(customer)
            elif customer_choice == "2":
                print("Going back to Customer Menu...")
                break
            else:
                print("\nInvalid choice. Please try again.")
        
    def manage_movies(self):
        print("\nManaging Movies and Schedules:")
        # Additional logic for managing movies goes here
        while True:
            print(f"{'1. Insert New Movie':<15}{'2. Edit Existing Movie':<15}{'3. Back to Admin Menu':<15}")
            admin_choice = input("Select an option: ")

            if admin_choice == "1":
                self.insert_new_movie()
            elif admin_choice == "2":
                self.edit_existing_movie()
            elif admin_choice == "3":
                break
            else:
                print("\nInvalid choice. Please try again.")
                
    def manage_customer_bookings(self):
        print("\nManaging Customer Bookings:")
        while True:
            print(f"{'1. View all bookings':<15}{'2. Edit booking':<15}{'3. Delete booking':<15}{'4. Back to Admin Menu'}")
            admin_choice = input("Select an option: ")

            if admin_choice == "1":
                self.view_all_customer_bookings()
            elif admin_choice == "2":
                self.edit_customer_booking()
            elif admin_choice == "3":
                self.delete_customer_booking()
            elif admin_choice == "4":
                print("Going back to Admin Menu...")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def insert_new_movie(self):
        print("\nInserting New Movie:")
        name = input("Enter movie name: ")
        director = input("Enter director name: ")
        release = input("Enter release date: ")
        language = input("Enter language: ")
        subtitle = input("Does the movie have subtitles? (Yes/No): ")
        rate = input("Enter movie rating: ")

        # Insert the new movie into the database
        insert_query = """INSERT INTO movies (name, director, release, language, subtitle, rate) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(insert_query, (name, director, release, language, subtitle, rate))
        self.connection.commit()

        print(f"\nMovie '{name}' has been successfully added!")

    def edit_existing_movie(self):
        print("\nEditing Existing Movie:")
        self.view_movies()
        movie_id = input("\nEnter the ID of the movie to edit: ")
        # Add additional checks to ensure the movie_id is valid
        try:
            # Validate that movie_id is a positive integer
            movie_id = int(movie_id)
            if movie_id <= 0:
                raise ValueError("Movie ID must be a positive integer.")
            
            # Fetch the existing movie details
            select_query = "SELECT * FROM movies WHERE id=?"
            self.cursor.execute(select_query, (movie_id,))
            movie_data = self.cursor.fetchone()

            if movie_data:
                # Display the existing details
                movie = Movie(*movie_data)
                print("\nExisting Movie Details:")
                print(f"ID: {movie.id}")
                print(f"Name: {movie.name}")
                print(f"Director: {movie.director}")
                print(f"Release Date: {movie.release}")
                print(f"Language: {movie.language}")
                print(f"Subtitle: {movie.subtitle}")
                print(f"Rating: {movie.rate}")

                # Prompt for new details
                name = input("\nEnter new movie name (press Enter to keep existing): ") or movie.name
                director = input("Enter new director name (press Enter to keep existing): ") or movie.director
                release = input("Enter new release date (press Enter to keep existing): ") or movie.release
                language = input("Enter new language (press Enter to keep existing): ") or movie.language
                subtitle = input("Does the movie have subtitles? (Yes/No, press Enter to keep existing): ") or movie.subtitle
                rate = input("Enter new movie rating (press Enter to keep existing): ") or movie.rate

                # Update the movie in the database
                update_query = """UPDATE movies SET name=?, director=?, release=?, language=?, subtitle=?, rate=? WHERE id=?"""
                self.cursor.execute(update_query, (name, director, release, language, subtitle, rate, movie_id))
                self.connection.commit()

                print(f"\nMovie with ID {movie_id} has been successfully updated!")

            else:
                print(f"\nMovie with ID {movie_id} not found. Please enter a valid movie ID.")
                
        except ValueError as e:
            print(f"\nError: {e}. Please enter a valid positive integer for Movie ID.")

    def view_all_customer_bookings(self):
        print("\nViewing All Customer Bookings:")
        # Fetch and display all customer bookings
        query = """SELECT booking.id, users.email, movies.name, rooms.number, seats.number, booking.date
            FROM booking
            JOIN users ON booking.users_id = users.id
            JOIN movies ON booking.movies_id = movies.id
            JOIN rooms ON booking.rooms_id = rooms.id
            JOIN seats ON booking.seats_id = seats.id
        """
        self.cursor.execute(query)
        bookings_data = self.cursor.fetchall()

        if bookings_data:
            print("\nAll Customer Bookings:")
            print(f"{'Booking ID':<12}{'Customer Email':<25}{'Movie Name':<30}{'Room Number':<15}{'Seat Number':<15}{'Date':<20}")
            print("-" * 120)
            for booking_data in bookings_data:
                print(f"{booking_data[0]:<12}{booking_data[1]:<25}{booking_data[2]:<30}{booking_data[3]:<15}{booking_data[4]:<15}{booking_data[5]:<20}")
            print("-" * 120)
        else:
            print("No customer bookings found.")

    def edit_customer_booking(self):
        print("\nEditing Customer Booking:")
        self.view_all_customer_bookings()
        booking_id = input("\nEnter the ID of the booking to edit: ")
        # Add additional checks to ensure the booking_id is valid
        try:
            # Validate that booking_id is a positive integer
            booking_id = int(booking_id)
            if booking_id <= 0:
                raise ValueError("Booking ID must be a positive integer.")
            
            # Fetch the existing booking details
            select_query = """
                SELECT booking.id, users.email, movies.name, rooms.number, seats.number, booking.date
                FROM booking
                JOIN users ON booking.users_id = users.id
                JOIN movies ON booking.movies_id = movies.id
                JOIN rooms ON booking.rooms_id = rooms.id
                JOIN seats ON booking.seats_id = seats.id
                WHERE booking.id=?
            """
            self.cursor.execute(select_query, (booking_id,))
            booking_data = self.cursor.fetchone()

            if booking_data:
                # Display the existing details
                print("\nExisting Booking Details:")
                print(f"Booking ID: {booking_data[0]}")
                print(f"Customer Email: {booking_data[1]}")
                print(f"Movie Name: {booking_data[2]}")
                print(f"Room Number: {booking_data[3]}")
                print(f"Seat Number: {booking_data[4]}")
                print(f"Date: {booking_data[5]}")

                # Prompt for new details
                new_date = input("\nEnter new booking date (press Enter to keep existing): ") or booking_data[5]

                # Update the booking in the database
                update_query = "UPDATE booking SET date=? WHERE id=?"
                self.cursor.execute(update_query, (new_date, booking_id))
                self.connection.commit()

                print(f"\nBooking with ID {booking_id} has been successfully updated!")

            else:
                print(f"\nBooking with ID {booking_id} not found. Please enter a valid booking ID.")
                
        except ValueError as e:
            print(f"\nError: {e}. Please enter a valid positive integer for Booking ID.")

    def delete_customer_booking(self):
        print("\nDeleting Customer Booking:")
        self.view_all_customer_bookings()
        booking_id = input("\nEnter the ID of the booking to delete: ")
        # Add additional checks to ensure the booking_id is valid
        try:
            # Validate that booking_id is a positive integer
            booking_id = int(booking_id)
            if booking_id <= 0:
                raise ValueError("Booking ID must be a positive integer.")
            
            # Delete the booking from the database
            delete_query = "DELETE FROM booking WHERE id=?"
            self.cursor.execute(delete_query, (booking_id,))
            self.connection.commit()

            print(f"\nBooking with ID {booking_id} has been successfully deleted!")
            
        except ValueError as e:
            print(f"\nError: {e}. Please enter a valid positive integer for Booking ID.")    

    def get_available_seats(self, movie_id, room_type_choice):
        # Fetch available seats based on movie_id and room_type_choice
        query = """
            SELECT seats.id, rooms.number, seats.number
            FROM seats
            JOIN rooms ON seats.rooms_id = rooms.id
            WHERE seats.reserved='No' AND rooms.type=?
        """
        self.cursor.execute(query, (room_type_choice,))
        return self.cursor.fetchall()    
    
    def view_customer_bookings(self, customer):
        print("\nViewing Your Bookings:")
        query = """
            SELECT tickets.id, movies.name, rooms.number, seats.number, tickets.date
            FROM tickets
            JOIN movies ON tickets.movies_id = movies.id
            JOIN rooms ON tickets.room_id = rooms.id
            JOIN seats ON tickets.seat_id = seats.id
            WHERE tickets.users_id=?
        """
        self.cursor.execute(query, (customer.id,))
        bookings_data = self.cursor.fetchall()

        if bookings_data:
            print("\nYour Bookings:")
            print(f"{'Ticket ID':<12}{'Movie Name':<30}{'Room Number':<15}{'Seat Number':<15}{'Date':<20}")
            print("-" * 92)
            for booking_data in bookings_data:
                print(f"{booking_data[0]:<12}{booking_data[1]:<30}{booking_data[2]:<15}{booking_data[3]:<15}{booking_data[4]:<20}")
            print("-" * 92)
        else:
            print("No bookings found.")
                                    
    def _del_(self):
        self.cursor.close()
