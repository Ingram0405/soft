    #  pylint: disable=missing-function-docstring
    #  pylint: disable=missing-class-docstring
    #  pylint: disable=missing-module-docstring

''' With this assignment seeing that: "It could well be the first project you 
    add to your developer portfolio!"  I decided to go a bit back into the 
    course and also add the functionality of a database for users.
    I am sure any bookstore would like security on their system. Here you can 
    use:
    User ID admin, password adm1n 
'''

import sqlite3  # Importing SQLite3
from colorama import Fore, init
init(autoreset=True)

# Create Database
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

#  Creating Table book
cursor.execute('''CREATE TABLE IF NOT EXISTS book
               (id INTEGER PRIMARY KEY,
               title TEXT, 
               author TEXT, 
               qty INTEGER)''')
db.commit()

#  Only adding books if table is Empty
cursor.execute("SELECT COUNT(*) FROM book")
if cursor.fetchone()[0] == 0:
    cursor.executemany('''INSERT INTO book (id, title, author, qty)
               VALUES (?,?,?,?)''',
    [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
    (3006, '1984', 'George Orwell', 20),
    (3007, 'The Great Gatsby', 'F. Scott Fitzgerald', 18),
    (3008, 'Pride and Prejudice', 'Jane Austen', 22),
    (3009, 'The Hobbit', 'J.R.R Tolkien', 15),
    (3010, 'The Catcher in the Rye', 'J.D. Salinger', 17)
])
db.commit()


cursor.execute('''CREATE TABLE IF NOT EXISTS
                  user_login(user_name TEXT PRIMARY KEY,
                  user_pass TEXT NOT NULL)''')  #  Creating a Database for users
db.commit()

# Here I am entering a default user to get started on the database table
cursor.execute('''INSERT OR IGNORE INTO user_login(user_name, user_pass)
               VALUES (?,?)''', ('admin', 'adm1n'))
db.commit()

# Below steps is to login for a user.
while True:
    user_name = input(Fore.BLUE + "\n ⛔ Please Enter your username or "
                      "select '0' to exit: ").strip()
    if user_name == "0":
        exit()

    cursor.execute("SELECT user_pass FROM user_login WHERE user_name = ?",
                   (user_name,))
    result = cursor.fetchone()

    if result:
        break
    else:
        print(Fore.RED + "⚠️ No matching user found. Please try again.")


while True:
    user_password = input("Please enter your password or select " \
                          "'0' to exit: ").strip()
    if user_password == "0":
        exit()

    if user_password == result[0]:  # result[0] holds the password from DB
        print(Fore.GREEN + f"\nWelcome {user_name.capitalize()} 😊")
        break
    else:
        print(Fore.RED + "Wrong password, try again or 'e' to exit.")

#  Different Menu Options for an Admin User
while True:

    if user_name == "admin":
        menu = input(Fore.CYAN + '''\nSelect one of the following options:
1 - Enter Book
2 - Update Book
3 - Delete a Book
4 - Search Books
5 - Exit
6 - Create a new User and Password
7 - Remove a User
: ''').strip()

#  Different Menu Option for normal Users.
    else:
        menu = input(Fore.CYAN + '''\nSelect one of the following options:
1 - Enter Book
2 - Update Book
3 - Delete a Book
4 - Search Books
5 - Exit
: ''').strip()

    # Creating a new user and password
    if menu == '6':
        while True:
            new_username = input(Fore.GREEN + "\nPlease enter a new " \
                                 "username, minimum 4 characters.")

            if len(new_username) < 4:
                print(Fore.RED + "Username must be at least 4 characters.")
                continue

            cursor.execute(
                "SELECT user_name FROM user_login" 
                "WHERE user_name = ?", (new_username,))

            if cursor.fetchone():

                print(Fore.RED + "\nThat Username already exists. "
                "Please try another:")
                continue
            break

        while True:
            new_password = input("Enter a new password "
                                "(min 6 characters): ").strip()

            if len(new_password) < 6:
                print(Fore.RED + "⚠️ Password must be at least 6 "
                                 "characters.")
                continue
            break

        # Insert the new user into the DB
        cursor.execute("INSERT INTO user_login (user_name, user_pass) "
                       "VALUES (?, ?)",(new_username, new_password))
        db.commit()

        print(Fore.GREEN + f"✅ User '{new_username}' successfully "
                            "registered!")

    #  Removing a User
    elif menu == '7':
        user_to_remove = input(Fore.YELLOW + "\nEnter the username "
                                             "to remove: ").strip()

        # Prevent deleting the admin account
        if user_to_remove == 'admin':
            print(Fore.RED + "⛔ You cannot delete the admin account.")
        else:
            cursor.execute(
                "SELECT user_name FROM user_login "
                "WHERE user_name = ?",
                (user_to_remove,)
            )

            if cursor.fetchone():
                confirm = input(
                        Fore.RED + f"Are you sure you want to delete user "
                                   f"'{user_to_remove}'? (y/n): "
                        ).strip()

                if confirm == 'y':
                    cursor.execute(
                        "DELETE FROM user_login WHERE user_name = ?",
                        (user_to_remove,)
                    )
                    db.commit()

                    print(Fore.GREEN + f"✅ User '{user_to_remove}' "
                                       f"has been removed.")

                else:
                    print(Fore.YELLOW + "❌ Wrong Option! "
                                        "Deletion cancelled.")
            else:
                print(Fore.RED + f"⚠️ User '{user_to_remove}' "
                                 f"not found.")

    #  Adding a new book into the database with ID numbers no less than 4 digits
    elif menu == '1':
        print(Fore.GREEN + "\n Enter the details for the new book: 📙")

        while True:
            try:
                new_id = int(input(Fore.BLUE + "Enter the book ID "
                                     "(Numbers Only) (4): ").strip())

                if new_id < 1000:
                    print(Fore.RED + "⛔ Book ID must be at least 4 "
                                     "digits (e.g. 1001 or higher).")
                    continue

                cursor.execute("SELECT * FROM book WHERE id = ?",
                               (new_id,))
                if cursor.fetchone():
                    print(Fore.RED + "❌ Book ID already exists, "
                                     "please try another ")
                    continue
                break
            except ValueError:
                print(Fore.RED + "⛔ Invalid ID, please enter a number!")

        new_title = input(Fore.GREEN + "Please enter a new Title 📖 :")
        new_author = input(Fore.GREEN + " Please enter the Author ✒️  :")

        while True:
            try:
                new_qty = int(input(Fore.CYAN + "How many books "
                                                "should I add? 🔢 :"))
                break
            except ValueError:
                print(Fore.RED + "❌ Please enter a valid Number!")

        cursor.execute(
            "INSERT INTO book (id, title, author, qty)"
            "VALUES (?, ?, ?, ?)",
            (new_id, new_title, new_author, new_qty)
        )
        db.commit()
        print(Fore.GREEN + f"✅ Book '{new_title}' by "
                           f"{new_author} added successfully.")

    #  Update a book, id, title or Author
    elif menu == '2':
        def show_book(book):
            print(Fore.GREEN + f"\n Book information:\n"
                f"ID {book[0]} | Title {book[1]} | Author{book[2]} | "
                f"Qty{book[3]}")
        try:
            book_id = int(input(Fore.GREEN + "\n Enter the ID to Update:"))
            cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
            book = cursor.fetchone()

            if not book:
                print(Fore.RED + "No book found with that ID ⛔")
            else:
                show_book(book)

                book_update ={}

                print(Fore.YELLOW + "\n Leave a field blank if you "
                                    "do not want to change it.🌌 ")

                new_title = input("New Title: ").strip()
                if new_title:
                    book_update["title"] = new_title

                new_author = input("New Author: ").strip()
                if new_author:
                    book_update["author"] = new_author

                new_qty = input("New Quantity: ").strip()
                if new_qty:
                    try:
                        book_update["qty"] = int(new_qty)
                    except ValueError:
                        print(Fore.RED + "Invalid quantity. Skipping "
                                         "quantity update. ⛔  ")
                if book_update:
                    for column, value in book_update.items():
                        cursor.execute(f"UPDATE book SET {column} = ? "
                                       f"WHERE id = ?", (value, book_id))
                    db.commit()
                    print(Fore.GREEN + "information updated "
                                       "successfully. 🍾")
                else:
                    print(Fore.RED + "No Updates were made!! 🙊 ")

        except ValueError:
            print(Fore.RED + "Please enter a number! 🔢 ")

    #  Remove a book from the Database
    elif menu == '3':
        try:
            del_book = int(input(Fore.LIGHTGREEN_EX + "\n Enter an ID of "
                                 "the book you would like to delete 📚:"))
            cursor.execute("SELECT * FROM book WHERE id = ?", (del_book,))
            book = cursor.fetchone()

            if not book:
                print(Fore.RED + f" No book with ID {del_book}.⛔")

            else:
                print(Fore.GREEN + f"\nBook to delete:"
                      f"ID: {book[0]} | Title: {book[1]} | Author: "
                      f"{book[2]} | Qty: {book[3]}")
                yes_no = input(Fore.RED + "Are you sure you want to "
                        "delete this book? 📖 (y/n): ").strip().lower()
                if yes_no == 'y':
                    cursor.execute(
                        "DELETE FROM book WHERE id = ?", (del_book,)
                        )
                    db.commit()
                    print(Fore.GREEN + "Your book has been deleted. ☠️")
                else:
                    print(Fore.CYAN + "Deletion cancelled.  ⛔")

        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number:  🔢")


    elif menu == '4':
        print(Fore.YELLOW + "\nSearch for a book:")
        print("1 - Search by ID 🔢 :")
        print("2 - Search by Title 📑 :")
        print("3 - Search by Author 👨👩 :")
        search_option = input("Select an option (1/2/3): ").strip()

        if search_option == '1':
            try:
                search_id = int(input("Enter the book ID: 🔢 :"))
                cursor.execute("SELECT * FROM book WHERE id = ?", 
                               (search_id,))
                book = cursor.fetchone()
                if book:
                    print(Fore.GREEN + f"\nID: {book[0]} | "
                          f"Title: {book[1]} | Author: {book[2]} | "
                          f"Qty: {book[3]}")
                else:
                    print(Fore.RED + "No book found with that ID. ❌")
            except ValueError:
                print(Fore.RED + "Invalid ID. Please enter a number 🔢 :")

        elif search_option == '2':
            search_title = input("Enter part of the title 📑 :").strip()
            cursor.execute(
                "SELECT * FROM book WHERE title LIKE ?", 
                ('%' + search_title + '%',)
                )
            books = cursor.fetchall()
            if books:
                print(Fore.GREEN + "\nResults:")
                for book in books:
                    print(f"ID: {book[0]} | Title: {book[1]} | "
                          f"Author: {book[2]} | Qty: {book[3]}")
            else:
                print(Fore.RED + "No books found with that title. ❌")

        elif search_option == '3':
            search_author = input("Enter part or all of the author's "
                                  "name 👨👩 :").strip()
            cursor.execute("SELECT * FROM book WHERE author LIKE ?",
                          ('%' + search_author + '%',))
            books = cursor.fetchall()
            if books:
                print(Fore.GREEN + "\nResults:")
                for book in books:
                    print(f"ID: {book[0]} | Title: {book[1]} | "
                          f"Author: {book[2]} | Qty: {book[3]}")
            else:
                print(Fore.RED + "No books found by that author. ❌")

        else:
            print(Fore.RED + "Invalid option. Please select "
                             "1, 2, or 3. ⛔")

    #  Exiting the program
    elif menu == '5':
        print('\nGoodbye!!! 👋\n')
        exit()

    else:
        print(Fore.RED +"\nYou have entered an invalid input. "
        "Please try again 👎")
