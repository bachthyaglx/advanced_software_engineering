import sqlite3
import datetime
from user import User, Customer, Admin
from movie import Movie

class System:
    def __init__(self, database="cinema.db"):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.customers = []

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email=? AND password=?"
        self.cursor.execute(query, (email, password))
        user_data = self.cursor.fetchone()

        if user_data:
            role = 'admin' if user_data[5] == 'No' else 'customer'
            return Admin(email, password) if role == 'admin' else Customer(email, password), role
        else:
            print('User not found. Please register an account!')
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
            print("\n1. Login\n2. Register\n3. Exit")
            choice = input("\nSelect an option: ")
        
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_registration()
            elif choice == "3":
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def handle_login(self):
        email = input("\nEnter email: ")
        password = input("Enter password: ")
        user, role = self.login(email, password)
        if user:
            print(f"\nWelcome, {email}! You are logged in as {role}.")
            self.handle_user_menu(user, role)
        else:
            print("\nUser not found. Please try again or register an account!")

    def handle_registration(self):
        firstname = input("\nFirstname: ")
        lastname = input("Lastname: ")
        email = input("Email: ")
        password = input("Password: ")
        new_customer = self.register_customer(firstname, lastname, email, password)
        print(f"\nAccount created for {email}. You can now log in.")

    def handle_user_menu(self, user, role):
        menu_options = {
            'customer': self.customer_menu,
            'admin': self.admin_menu
        }
        while True:
            print("\n1. View Movies and Showtimes\n2. Book a Seat\n3. Manage Bookings\n4. Logout")
            user_choice = input("\nSelect an option: ")
            menu_func = menu_options.get(role)
            if menu_func:
                menu_func(user)
            elif user_choice == "4":
                print("\nLogging out...")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def customer_menu(self, customer):
        while True:
            print("\n1. View Movies and Showtimes\n2. Book a Seat\n3. Manage Bookings\n4. Logout")
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
            print("\n1. View Movies and Showtimes\n2. Manage Movies and Schedules\n3. Manage Customer Bookings\n4. Logout")
            admin_choice = input("\nSelect an option: ")

            if admin_choice == "1":
                self.view_movies()
            elif admin_choice == "2":
                self.manage_movies()
            elif admin_choice == "3":
                self.manage_customer_bookings()
            elif admin_choice == "4":
                print("\nLogging out...")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def view_movies(self):
        query = "SELECT * FROM movies"
        self.cursor.execute(query)
        movies_data = self.cursor.fetchall()
        movies = [Movie(*movie_data) for movie_data in movies_data]
        
        print(f"\n{'-' * 70}")
        print(f"{'No':<5}{'Name':<30}{'Language':<15}{'Release':<10}")
        print(f"{'-' * 70}")
        for movie in movies:
            print(f"{movie.id:<5}{movie.name:<30}{movie.language:<15}{movie.release:<10}")
        print(f"{'-' * 70}")
            
    def book_ticket(self, customer):
        print("\nBooking a Ticket:")
        self.view_movies()

        movie_id = input("\nSelect a movie (enter movie ID): ")
        try:
            movie_id = int(movie_id)
            if movie_id <= 0:
                raise ValueError("Movie ID must be a positive integer.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid positive integer for Movie ID.")
            return

        room_type_choice = input("\nSelect a room type (enter room type number): ")

        available_seats = self.get_available_seats(movie_id, room_type_choice)

        if not available_seats:
            print("No available seats for the selected room type.")
            return

        print("\nAvailable Seats:")
        for seat in available_seats:
            print(f"Seat ID: {seat[0]}, Room Number: {seat[1]}, Seat Number: {seat[2]}")

        seat_id = input("\nSelect a seat (enter seat ID): ")
        try:
            seat_id = int(seat_id)
            if seat_id <= 0:
                raise ValueError("Seat ID must be a positive integer.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid positive integer for Seat ID.")
            return

        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_ticket_query = """INSERT INTO tickets (users_id, movies_id, room_id, seat_id, date) VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(insert_ticket_query, (customer.id, movie_id, seat[0], seat[1], current_date))
        self.connection.commit()

        print("\nTicket booked successfully!")
        
    def manage_bookings(self, customer):
        print("\nManaging Bookings:")
        while True:
            print("\n1. View Your Bookings\n2. Back to Customer Menu")
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
        while True:
            print("\n1. Insert New Movie\n2. Edit Existing Movie\n3. Back to Admin Menu")
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
            print("\n1. View all bookings\n2. Edit booking\n3. Delete booking\n4. Back to Admin Menu")
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
                print(f"Release Date: {movie.release}")
                print(f"Language: {movie.language}")
                print(f"Subtitle: {movie.subtitle}")
                print(f"Rating: {movie.rate}")

                name = input("\nEnter new movie name (press Enter to keep existing): ") or movie.name
                director = input("Enter new director name (press Enter to keep existing): ") or movie.director
                release = input("Enter new release date (press Enter to keep existing): ") or movie.release
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

    def view_all_customer_bookings(self):
        print("\nViewing All Customer Bookings:")
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

    def get_available_seats(self, movie_id, room_type_choice):
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
