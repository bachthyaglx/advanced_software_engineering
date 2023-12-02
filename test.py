import sqlite3

try:
    sqliteConnection = sqlite3.connect('cinema.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    firstname = input("Firstname: ")
    lastname = input("Lastname: ")
    email = input("Email: ")
    password = input("Password: ")
      
    insert_query = """INSERT INTO users (firstname, lastname, email, password) VALUES (?,?,?,?)"""
                
    cursor.execute(insert_query, (firstname, lastname, email, password))
    
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")