import os
import keyboard
import sqlite3
import time
import datetime
from user import Customer, Admin
from movie import Movie

class System:
    # Setup MESS
    SELECT_OPTION_PROMPT = "\n\nSelect an option: "
    INVALID_CHOICE_MESSAGE = "\nInvalid choice. Please try again."
        
    def __init__(self, database="cinema.db"):
        # Initialize login status attribute
        self.logged_in_user = None
        
        try:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            self.customers = []
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def clear_screen(self):
        if os.name == 'posix':
            # For Unix/Linux/MacOS
            os.system('clear')
        elif os.name == 'nt':
            # For Windows
            os.system('cls')
    
    def back_to_previous_menu(self):
        print(f"\nESC. Back to previous menu")
        while True:
            if(keyboard.is_pressed('esc')):
                self.clear_screen()
                break

    def run(self):
        while True:
            self.clear_screen()
            print("\nWelcome to our Cinema! Latest movies:")
            self.view_movies()
            print(f"\n1. Login\n2. Register\n3. Exit" + self.SELECT_OPTION_PROMPT)
            choice = input()
            if choice == "1":
                self.clear_screen()
                self.handle_login()
            elif choice == "2":
                self.clear_screen()
                self.handle_registration()
            elif choice == "3":
                self.clear_screen()
                print("\nGoodbye!\n")
                quit()
            else:
                self.clear_screen()

    def login(self, email, password):
        try:
            query = "SELECT * FROM users WHERE email=? AND password=?"
            self.cursor.execute(query, (email, password))
            user_data = self.cursor.fetchone()

            if user_data:
                role = 'admin' if user_data[5] == 'No' else 'customer'
                return Admin(email, password) if role == 'admin' else Customer(email, password), role
            else:
                print('User not found. Please register an account!')
                return None, None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None, None
        
    def handle_login(self):
        try:
            email = input("\nEnter email: ")
            password = input("Enter password: ")
            user, role = self.login(email, password)
            if user:
                print(f"\nWelcome, {email}! You are logged in as {role}.")
                self.logged_in_user = user
                self.handle_user_menu(user, role)
            else:
                print("\nUser not found. Please try again or register an account!")
        except KeyboardInterrupt:
            print("\nLogin process interrupted by the user.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
            
    def register_customer(self, firstname, lastname, email, password):
        try:
            insert_query = """INSERT INTO users (firstname, lastname, email, password) VALUES (?,?,?,?)"""
            self.cursor.execute(insert_query, (firstname, lastname, email, password))
            self.connection.commit()
            
            return Customer(email, password)
        except sqlite3.IntegrityError:
            print("User with this email already exists. Please choose another email.")
            return None

    def handle_registration(self):
        firstname = input("\nFirstname: ")
        lastname = input("Lastname: ")
        email = input("Email: ")
        password = input("Password: ")
        self.register_customer(firstname, lastname, email, password)
        print(f"\nAccount created for {email}. You can now log in.")

    def handle_user_menu(self, user, role):
        menu_options = {
            'customer': self.customer_menu,
            'admin': self.admin_menu
        }
        menu_func = menu_options.get(role)
        if menu_func:
            menu_func(user)

    def customer_menu(self, customer):
        while True:
            self.clear_screen()
            print(f"\nHello! " + customer.email)
            print("\n1. View movies and showtimes\n2. Book a ticket\n3. Manage bookings\n4. Logout" + self.SELECT_OPTION_PROMPT)
            customer_choice = input()

            if customer_choice == "1":
                self.clear_screen()
                self.view_movies()
                self.back_to_previous_menu()
            elif customer_choice == "2":
                self.clear_screen()
                self.book_ticket(customer)
            elif customer_choice == "3":
                self.clear_screen()
                self.manage_bookings(customer)
            elif customer_choice == "4":
                print("\nLogging out...")
                self.logged_in_user = None
                return self.run()
        
    def admin_menu(self, admin):
        while True:
            self.clear_screen()
            print("\n1. View Movies and Showtimes\n2. Manage Movies and Schedules\n3. Manage Customer Bookings\n4. Logout" + self.SELECT_OPTION_PROMPT)
            admin_choice = input()

            if admin_choice == "1":
                self.clear_screen()
                self.view_movies()
                self.back_to_previous_menu()
            elif admin_choice == "2":
                self.clear_screen()
                self.manage_movies()
            elif admin_choice == "3":
                self.clear_screen()
                self.manage_customer_bookings()
            elif admin_choice == "4":
                print("\nLogging out...")
                self.logged_in_user = None
                self.clear_screen()
                return self.run()
            else:
                self.clear_screen()

    def view_movies(self):
        self.cursor.execute("SELECT * FROM movies")
        movies_data = self.cursor.fetchall()
        movies = [Movie(*movie_data) for movie_data in movies_data]
            
        print(f"\n{'-' * 70}")
        print(f"{'ID':<5}{'Name':<30}{'Language':<15}{'Release Date':<15}")  # Update column header
        print(f"{'-' * 70}")
        for movie in movies:
            print(f"{movie.id:<5}{movie.name:<30}{movie.language:<15}{movie.release_date:<15}")  # Update column name
        print(f"{'-' * 70}")
            
    def book_ticket(self, customer):
        print("\nBooking a ticket")
        self.view_movies()

        self.cursor.execute("SELECT * FROM movies")
        movies_data = self.cursor.fetchall()
        movies = [Movie(*movie_data) for movie_data in movies_data]

        movie_id = input("\nSelect a movie (enter movie ID): ")
        valid_movie_ids = [str(movie.id) for movie in movies]  # Get list of valid movie IDs as strings

        while movie_id not in valid_movie_ids:
            print("Error: Invalid movie ID. Please enter a valid movie ID.")
            movie_id = input("\nSelect a movie (enter movie ID): ")

        room_type = input("\nSelect a room type (2D or 3D): ").strip().upper()

        while room_type not in ["2D", "3D"]:
            print("Error: Invalid room type. Please enter either '2D' or '3D'.")
            room_type = input("\nSelect a room type (2D or 3D): ").strip().upper()

        available_seats_query = """
            SELECT seats.id, rooms.number, seats.number
            FROM seats
            JOIN rooms ON seats.rooms_id = rooms.id
            JOIN movies ON rooms.movies_id = movies.id
            WHERE seats.reserved='No' AND rooms.type=? AND movies.id=?
        """

        self.cursor.execute(available_seats_query, (room_type, movie_id))
        available_seats_data = self.cursor.fetchall()

        if not available_seats_data:
            print("No available seats for the selected room type.")
            return

        print("\nAvailable Seats:")
        for seat_data in available_seats_data:
            print(f"Seat ID: {seat_data[0]}, Room Number: {seat_data[1]}, Seat Number: {seat_data[2]}")

        available_seat_ids = [str(seat_data[0]) for seat_data in available_seats_data]
       
        while True:
                seat_id = input("\nSelect a seat (enter seat ID): ")

                if seat_id in available_seat_ids:
                    break
                else:
                    print("Error: Invalid seat ID. Please enter a valid seat ID.")

        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Fetching the first available seat's room number and seat number
        room_number = available_seats_data[0][1]
        # Fetch customer.id
        customer_id_querry = """SELECT id from users where email=?"""

        self.cursor.execute(customer_id_querry, (customer.email,))
        customer_id = self.cursor.fetchone()[0]

        insert_ticket_query = """INSERT INTO tickets (users_id, movies_id, room_id, seat_id, date) VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(insert_ticket_query, (customer_id, movie_id, room_number, seat_id, current_date))
        self.connection.commit()

        print("\nTicket booked successfully!")
        print("\nReturing to previous menu in 10s...")
        time.sleep(10)
        
    def manage_bookings(self, customer):
        print("\nManaging Bookings:")
        while True:
            print("\n1. View Your Bookings\n2. Back to Customer Menu" + self.SELECT_OPTION_PROMPT)
            customer_choice = input()

            if customer_choice == "1":
                self.clear_screen()
                self.view_customer_bookings(customer)
                self.back_to_previous_menu()
            elif customer_choice == "2":
                self.clear_screen()
                break
            else:
                self.clear_screen()
        
    def manage_movies(self):
        print("\nManaging Movies and Schedules:")
        while True:
            self.clear_screen()
            print("\n1. Insert new movie\n2. Edit existing movie\n3. Back to admin menu" + self.SELECT_OPTION_PROMPT)
            admin_choice = input()

            if admin_choice == "1":
                self.clear_screen()
                self.insert_new_movie()
            elif admin_choice == "2":
                self.clear_screen()
                self.edit_existing_movie()
            elif admin_choice == "3":
                self.clear_screen()
                break
            else:
                self.clear_screen()
                
    def manage_customer_bookings(self):
        print("\nManaging Customer Bookings:")
        while True:
            print("\n1. View all bookings\n2. Edit booking\n3. Delete booking\n4. Back to Admin Menu" + + self.SELECT_OPTION_PROMPT)
            admin_choice = input()

            if admin_choice == "1":
                self.clear_screen()
                self.view_all_customer_bookings()
            elif admin_choice == "2":
                self.clear_screen()
                self.edit_customer_booking()
            elif admin_choice == "3":
                self.clear_screen()
                self.delete_customer_booking()
            elif admin_choice == "4":
                self.clear_screen()
                break
            else:
                self.clear_screen()

    def insert_new_movie(self):
        print("\nInserting New Movie:")
        name = input("Enter movie name: ")
        director = input("Enter director name: ")
        release = input("Enter release date: ")
        language = input("Enter language: ")
        subtitle = input("Does the movie have subtitles? (Yes/No): ")
        rate = input("Enter movie rating: ")

        insert_query = """INSERT INTO movies (name, director, release, language, subtitle, rate) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(insert_query, (name, director, release, language, subtitle, rate))
        self.connection.commit()

        print(f"\nMovie '{name}' has been successfully added!")

    def edit_existing_movie(self):
        print("\nEditing Existing Movie:")
        self.view_movies()
        movie_id = input("\nEnter the ID of the movie to edit: ")
        try:
            movie_id = int(movie_id)
            if movie_id <= 0:
                raise ValueError("Movie ID must be a positive integer.")
            
            select_query = "SELECT * FROM movies WHERE id=?"
            self.cursor.execute(select_query, (movie_id,))
            movie_data = self.cursor.fetchone()

            if movie_data:
                movie = Movie(*movie_data)
                print("\nExisting Movie Details:")
                print(f"ID: {movie.id}")
                print(f"Name: {movie.name}")
                print(f"Director: {movie.director}")
                print(f"Release Date: {movie.release_date}")
                print(f"Language: {movie.language}")
                print(f"Subtitle: {movie.subtitle}")
                print(f"Rating: {movie.rate}")

                name = input("\nEnter new movie name (press Enter to keep existing): ") or movie.name
                director = input("Enter new director name (press Enter to keep existing): ") or movie.director
                release = input("Enter new release date (press Enter to keep existing): ") or movie.release_date
                language = input("Enter new language (press Enter to keep existing): ") or movie.language
                subtitle = input("Does the movie have subtitles? (Yes/No, press Enter to keep existing): ") or movie.subtitle
                rate = input("Enter new movie rating (press Enter to keep existing): ") or movie.rate

                update_query = """UPDATE movies SET name=?, director=?, release=?, language=?, subtitle=?, rate=? WHERE id=?"""
                self.cursor.execute(update_query, (name, director, release, language, subtitle, rate, movie_id))
                self.connection.commit()

                print(f"\nMovie with ID {movie_id} has been successfully updated!")

            else:
                print(f"\nMovie with ID {movie_id} not found. Please enter a valid movie ID.")
                
        except ValueError as e:
            print(f"\nError: {e}. Please enter a valid positive integer for Movie ID.")
            
    def view_customer_bookings(self, customer):
        print("\nViewing Your Bookings:")
        # Fetch customer.id
        customer_id_querry = """SELECT id from users where email=?"""
        self.cursor.execute(customer_id_querry, (customer.email,))
        customer_id = self.cursor.fetchone()[0]
        
        query = """SELECT tickets.id, movies.name, rooms.number, seats.number, tickets.date
            FROM tickets
            JOIN movies ON tickets.movies_id = movies.id
            JOIN rooms ON tickets.room_id = rooms.id
            JOIN seats ON tickets.seat_id = seats.id
            JOIN users ON tickets.users_id = users.id
            WHERE tickets.users_id = ?
        """
        self.cursor.execute(query, (customer_id,))
        bookings_data = self.cursor.fetchall()[0]

        if bookings_data:
            print(f"\n{'Booking ID':<12}{'Movie Name':<30}{'Room Number':<15}{'Seat Number':<15}{'Date':<20}")
            print("-" * 100)
            print(f"{bookings_data[0]:<12}{bookings_data[1]:<30}{bookings_data[2]:<15}{bookings_data[3]:<15}{bookings_data[4]:<20}")
            print("-" * 100)
        else:
            print("\nYou have no bookings.")

    def view_all_customer_bookings(self):
        print("\nViewing All Customer Bookings:")
        query = """SELECT bookings.id, users.email, movies.name, rooms.number, seats.number, bookings.date
            FROM bookings
            JOIN users ON bookings.users_id = users.id
            JOIN movies ON bookings.movies_id = movies.id
            JOIN rooms ON bookings.rooms_id = rooms.id
            JOIN seats ON bookings.seats_id = seats.id
        """
        self.cursor.execute(query)
        bookings_data = self.cursor.fetchall()

        if bookings_data:
            print("\nAll Customer Bookings:")
            print(f"{'Booking ID':<12}{'Customer Email':<40}{'Movie Name':<30}{'Room Number':<30}{'Seat Number':<20}{'Date':<40}")
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
        try:
            booking_id = int(booking_id)
            if booking_id <= 0:
                raise ValueError("Booking ID must be a positive integer.")
            
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
                print("\nExisting Booking Details:")
                print(f"Booking ID: {booking_data[0]}")
                print(f"Customer Email: {booking_data[1]}")
                print(f"Movie Name: {booking_data[2]}")
                print(f"Room Number: {booking_data[3]}")
                print(f"Seat Number: {booking_data[4]}")
                print(f"Date: {booking_data[5]}")

                new_date = input("\nEnter new booking date (press Enter to keep existing): ") or booking_data[5]

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
        try:
            booking_id = int(booking_id)
            if booking_id <= 0:
                raise ValueError("Booking ID must be a positive integer.")
            
            delete_query = "DELETE FROM booking WHERE id=?"
            self.cursor.execute(delete_query, (booking_id,))
            self.connection.commit()

            print(f"\nBooking with ID {booking_id} has been successfully deleted!")
            
        except ValueError as e:
            print(f"\nError: {e}. Please enter a valid positive integer for Booking ID.")    

    def get_available_seats(self, room_type_choice):
        query = """
            SELECT seats.id, rooms.number, seats.number
            FROM seats
            JOIN rooms ON seats.rooms_id = rooms.id
            WHERE seats.reserved='No' AND rooms.type=?
        """
        self.cursor.execute(query, (room_type_choice,))
        return self.cursor.fetchall()    

    def __del__(self):
        try:
            self.cursor.close()
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")