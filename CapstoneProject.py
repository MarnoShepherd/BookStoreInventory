import sqlite3

# Function to connect to the database
def connect_to_database():
    conn = sqlite3.connect("ebookstore.db")
    return conn

# Function to create the table
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    Title TEXT NOT NULL,
                    Author TEXT NOT NULL,
                    Qty INTEGER NOT NULL
                    )''')
    conn.commit()

# Function to populate the table
def populate_table(conn):
    cursor = conn.cursor()
    books_data = [
        (3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
        (3005, "Alice in Wonderland", "Lewis Carroll", 12),
        # You can add more books here
    ]
    cursor.executemany("INSERT INTO books (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", books_data)
    conn.commit()

# Function to add a new book to the database
def add_book(conn, book_data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (Title, Author, Qty) VALUES (?, ?, ?)", book_data)
    conn.commit()

# Function to update book information
def update_book(conn, book_id, new_qty):
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET Qty = ? WHERE id = ?", (new_qty, book_id))
    conn.commit()

# Function to delete a book from the database
def delete_book(conn, book_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()

# Function to search for a specific book
def search_book(conn, title):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE Title LIKE ?", ('%' + title + '%',))
    return cursor.fetchall()

# Main function to run the program
def main():
    conn = connect_to_database()
    create_table(conn)
    populate_table(conn)

    while True:
        print("\nBookstore Clerk Menu:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("0. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            title = input("Enter the title: ")
            author = input("Enter the author: ")
            qty = int(input("Enter the quantity: "))
            add_book(conn, (title, author, qty))
            print("Book added successfully.")

        elif choice == 2:
            book_id = int(input("Enter the book ID: "))
            new_qty = int(input("Enter the new quantity: "))
            update_book(conn, book_id, new_qty)
            print("Book information updated successfully.")

        elif choice == 3:
            book_id = int(input("Enter the book ID: "))
            delete_book(conn, book_id)
            print("Book deleted successfully.")

        elif choice == 4:
            title = input("Enter the book title (or part of it): ")
            books = search_book(conn, title)
            if books:
                print("Search results:")
                for book in books:
                    print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Qty: {book[3]}")
            else:
                print("No books found matching the search criteria.")

        elif choice == 0:
            break

        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
