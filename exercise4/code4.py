import sqlite3

# Connect to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create Books table
c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID TEXT PRIMARY KEY,
             Title TEXT,
             Author TEXT,
             ISBN TEXT,
             Status TEXT)''')

# Create Users table
c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID TEXT PRIMARY KEY,
             Name TEXT,
             Email TEXT)''')

# Create Reservations table
c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID TEXT PRIMARY KEY,
             BookID TEXT,
             UserID TEXT,
             ReservationDate TEXT)''')

# Function to add a new book to the database
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")
    
    c.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")

# Function to find a book's detail based on BookID
def find_book_detail():
    book_id = input("Enter BookID: ")
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.Status, Users.UserID, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))
    result = c.fetchone()
    if result:
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("Status:", result[3])
        if result[4]:
            print("Reserved by:")
            print(" UserID:", result[4])
            print(" Name:", result[5])
            print(" Email:", result[6])
    else:
        print("Book not found!")

# Function to find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    search_text = input("Enter BookID, Title, UserID, or ReservationID: ")
    if search_text.startswith("LB"):
        # Search by BookID
        c.execute("SELECT * FROM Books WHERE BookID = ?", (search_text,))
        result = c.fetchone()
        if result:
            print("Reservation status for BookID", result[0])
            print("Status:", result[4])
        else:
            print("Book not found!")
    elif search_text.startswith("LU"):
        # Search by UserID
        c.execute('''SELECT Books.BookID, Books.Status
                     FROM Books
                     JOIN Reservations ON Books.BookID = Reservations.BookID
                     WHERE Reservations.UserID = ?''', (search_text,))
        result = c.fetchall()
        if result:
            print("Reservation status for UserID", search_text)
            for row in result:
                print("BookID:", row[0])
                print("Status:", row[1])
        else:
            print("User not found or no reservations found for the user!")
    elif search_text.startswith("LR"):
        # Search by ReservationID
        c.execute('''SELECT Books.BookID, Books.Status, Users.UserID, Users.Name, Users.Email
                     FROM Books
                     JOIN Reservations ON Books.BookID = Reservations.BookID
                     JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Reservations.ReservationID = ?''', (search_text,))
        result = c.fetchone()
        if result:
            print("Reservation status for ReservationID", search_text)
            print("BookID:", result[0])
            print("Status:", result[1])
            print("UserID:", result[2])
            print("Name:", result[3])
            print("Email:", result[4])
        else:
            print("Reservation not found!")
    else:
        # Search by Title
        c.execute('''SELECT Books.BookID, Books.Status, Users.UserID, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.Title = ?''', (search_text,))
        result = c.fetchall()
        if result:
            print("Reservation status for Title", search_text)
            for row in result:
                print("BookID:", row[0])
                print("Status:", row[1])
                if row[2]:
                    print("Reserved by:")
                    print(" UserID:", row[2])
                    print(" Name:", row[3])
                    print(" Email:", row[4])
                print("-------------")
        else:
            print("Book not found!")

# Function to find all the books in the database
def find_all_books():
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationDate
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    result = c.fetchall()
    if result:
        for row in result:
            print("BookID:", row[0])
            print("Title:", row[1])
            print("Author:", row[2])
            print("Status:", row[3])
            if row[4]:
                print("Reserved by:")
                print(" UserID:", row[4])
                print(" Name:", row[5])
                print(" Email:", row[6])
            print("Reservation Date:", row[7])
            print("-------------")
    else:
        print("No books found!")

# Function to modify/update book details based on BookID
def modify_book_details():
    book_id = input("Enter BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = c.fetchone()
    if result:
        print("Book found. Current details:")
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        choice = input("Do you want to update the reservation status? (y/n): ")
        if choice.lower() == "y":
            new_status = input("Enter the new reservation status: ")
            c.execute('''UPDATE Books
                         SET Status = ?
                         WHERE BookID = ?''', (new_status, book_id))
            c.execute('''UPDATE Reservations
                         SET Status = ?
                         WHERE BookID = ?''', (new_status, book_id))
        else:
            new_title = input("Enter the new title: ")
            new_author = input("Enter the new author: ")
            new_isbn = input("Enter the new ISBN: ")
            c.execute('''UPDATE Books
                         SET Title = ?, Author = ?, ISBN = ?
                         WHERE BookID = ?''', (new_title, new_author, new_isbn, book_id))
        conn.commit()
        print("Book details updated successfully!")
    else:
        print("Book not found!")

# Function to delete a book based on its BookID
def delete_book():
    book_id = input("Enter BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = c.fetchone()
    if result:
        c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found!")

# Main program loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's detail")
    print("3. Find a book's reservation status")
    print("4. Find all the books")
    print("5. Modify/update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_detail()
    elif choice == "3":
        find_reservation_status() 
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        modify_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 7.")

# Close the database connection
conn.close()
