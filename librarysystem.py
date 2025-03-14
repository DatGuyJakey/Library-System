class User:
    def __init__(self, user_id, name, email, password):
        # Initialize the user with their ID, name, email, and password
        self.user_id = user_id
        self.name = name
        self.email = email
        self.__password = password  # Encapsulation of password

    def login(self, email, password, user_list):
        # Login function to verify user credentials by checking against the user_list
        for user in user_list:
            if user.email == email and user.__password == password:
                print(f"Welcome, {user.name}!")  # Successful login message
                return user  # Return the user object if login is successful
        print("Login failed! Incorrect email or password.")  # If no match found
        return None  # Return None if no matching user is found

    def logout(self):
        # Function to log the user out and print a message
        print(f"{self.name} has logged out.")


class Member(User):
    def __init__(self, user_id, name, email, password):
        # Inherit from User class and initialize additional Member-specific attributes
        super().__init__(user_id, name, email, password)
        self.borrowed_books = []  # List to store borrowed books
        self.reserved_books = []  # List to store reserved books

    def borrow_book(self, book):
        # Function for a member to borrow a book if available and borrowing limit is not reached
        if len(self.borrowed_books) < 5:
            if book.status == "Available":
                self.borrowed_books.append(book)
                book.update_status("Borrowed")  # Update the book's status to borrowed
                print(f"'{book.title}' has been borrowed!")  # Success message
            else:
                print(f"'{book.title}' is currently unavailable.")  # If book is not available
        else:
            print("You have reached your borrowing limit.")  # If borrowing limit is reached

    def return_book(self, book):
        # Function for a member to return a borrowed book
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_status("Available")  # Update the book's status to available
            print(f"'{book.title}' has been returned.")  # Success message
        else:
            print(f"You did not borrow '{book.title}'.")  # If book wasn't borrowed

    def reserve_book(self, book):
        # Function for a member to reserve a book if available and not already reserved
        if book.status == "Available" and book not in self.reserved_books:
            self.reserved_books.append(book)
            print(f"'{book.title}' has been reserved.")  # Success message
        else:
            print(f"'{book.title}' is unavailable or already reserved.")  # If book can't be reserved


class Librarian(User):
    def add_book(self, book_list, book):
        # Function for a librarian to add a new book to the library's book list
        book_list.append(book)
        print(f"'{book.title}' has been added to the library.")  # Success message


class Administrator(User):
    def manage_users(self, user_list, action, user=None):
        # Function for an administrator to add or remove users from the system
        if action == "add" and user:
            user_list.append(user)
            print(f"'{user.name}' has been added to the system.")  # Success message
        elif action == "remove" and user in user_list:
            user_list.remove(user)
            print(f"'{user.name}' has been removed from the system.")  # Success message


class Book:
    def __init__(self, book_id, title, author):
        # Initialize the book with its ID, title, author, and default status as "Available"
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = "Available"

    def update_status(self, new_status):
        # Function to update the status of a book (e.g., "Available", "Borrowed")
        self.status = new_status


# Simulate a simple command-line interface for interaction

# Create books, users, and a library
book_list = []
book1 = Book(101, "1984", "George Orwell")
book2 = Book(102, "Brave New World", "Aldous Huxley")
book3 = Book(103, "The Great Gatsby", "F. Scott Fitzgerald")
book_list.extend([book1, book2, book3])  # Add books to the library

# Create user roles (member, librarian, admin)
user_list = []
member1 = Member(1, "Jake", "jake@example.com", "password123")
librarian1 = Librarian(2, "Librarian", "librarian@example.com", "librarian123")
admin1 = Administrator(3, "Admin", "admin@example.com", "admin123")

# Admin adds the initial users (members, librarians, admins) to the system
admin1.manage_users(user_list, "add", member1)
admin1.manage_users(user_list, "add", librarian1)
admin1.manage_users(user_list, "add", admin1)

# Simple interactive loop for library system
while True:
    print("\nLibrary System")
    print("1. Login as Member")
    print("2. Login as Librarian")
    print("3. Login as Admin")
    print("4. Exit")
    choice = input("Select an option: ")

    if choice == "1":
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = User(0, "", "", "")  # Create a temporary user object for login check
        user = user.login(email, password, user_list)
        if user:
            if isinstance(user, Member):
                while True:
                    print("\nMember Actions")
                    print("1. Borrow Book")
                    print("2. Return Book")
                    print("3. Reserve Book")
                    print("4. Logout")
                    action = input("Choose an action: ")

                    if action == "1":
                        print("Available books:")
                        for book in book_list:
                            print(f"{book.title} - {book.status}")
                        book_title = input("Enter book title to borrow: ")
                        book_to_borrow = next((book for book in book_list if book.title == book_title), None)
                        if book_to_borrow:
                            user.borrow_book(book_to_borrow)
                        else:
                            print("Book not found.")
                    elif action == "2":
                        print("Borrowed books:")
                        for book in user.borrowed_books:
                            print(f"{book.title}")
                        book_title = input("Enter book title to return: ")
                        book_to_return = next((book for book in user.borrowed_books if book.title == book_title), None)
                        if book_to_return:
                            user.return_book(book_to_return)
                        else:
                            print("Book not found in borrowed books.")
                    elif action == "3":
                        print("Available books:")
                        for book in book_list:
                            print(f"{book.title} - {book.status}")
                        book_title = input("Enter book title to reserve: ")
                        book_to_reserve = next((book for book in book_list if book.title == book_title), None)
                        if book_to_reserve:
                            user.reserve_book(book_to_reserve)
                        else:
                            print("Book not found.")
                    elif action == "4":
                        user.logout()
                        break
                    else:
                        print("Invalid action.")
            else:
                print("You must log in as a member to perform this action.")
    elif choice == "2":
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = User(0, "", "", "")  # Create a temporary user object for login check
        user = user.login(email, password, user_list)
        if user:
            if isinstance(user, Librarian):
                while True:
                    print("\nLibrarian Actions")
                    print("1. Add Book")
                    print("2. Logout")
                    action = input("Choose an action: ")

                    if action == "1":
                        title = input("Enter book title: ")
                        author = input("Enter book author: ")
                        book_id = len(book_list) + 1
                        new_book = Book(book_id, title, author)
                        librarian1.add_book(book_list, new_book)
                    elif action == "2":
                        librarian1.logout()
                        break
                    else:
                        print("Invalid action.")
            else:
                print("You must log in as a librarian to perform this action.")
    elif choice == "3":
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = User(0, "", "", "")  # Create a temporary user object for login check
        user = user.login(email, password, user_list)
        if user:
            if isinstance(user, Administrator):
                while True:
                    print("\nAdmin Actions")
                    print("1. Add User")
                    print("2. Remove User")
                    print("3. Logout")
                    action = input("Choose an action: ")

                    if action == "1":
                        name = input("Enter user name: ")
                        email = input("Enter user email: ")
                        password = input("Enter user password: ")
                        user_id = len(user_list) + 1
                        new_member = Member(user_id, name, email, password)
                        admin1.manage_users(user_list, "add", new_member)
                    elif action == "2":
                        print("Current Users:")
                        for user in user_list:
                            print(f"{user.name} ({user.email})")
                        email = input("Enter email of user to remove: ")
                        user_to_remove = next((user for user in user_list if user.email == email), None)
                        if user_to_remove:
                            admin1.manage_users(user_list, "remove", user_to_remove)
                        else:
                            print("User not found.")
                    elif action == "3":
                        admin1.logout()
                        break
                    else:
                        print("Invalid action.")
            else:
                print("You must log in as an admin to perform this action.")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
