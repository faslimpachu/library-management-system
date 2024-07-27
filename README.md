USERS
1.	SUPERUSER
    User-name = admin
    Password = admin

2.	COUSTOMER
•	User-name = faslim
•	Password = Pachu@kozhikode

•	User-name = testuser1
•	Password = Kozhikode@123

   you can create new user for fresh usage 
    
Features Implemented
1.	Models:
o	User: Custom user model extending AbstractUser with fields is_librarian(superuser) and is_customer.
o	Author: Model to store author details.
o	BookShelf: Model to store bookshelf location.
o	Book: Model to store book details, including a foreign key to Author and BookShelf.
o	History: Model to track the history of borrowed books.
o	BookRequest: Model to handle book requests and their statuses.
2.	Signals:
o	Automatically creates or updates an entry in the History model whenever a BookRequest status is changed to 'approved' or 'returned'.
3.	Middleware:
o	EncryptionMiddleware: Encrypts user emails based on a setting.
o	LoginRequiredMiddleware: Redirects non-authenticated users to the login page.
4.	Authentication:
o	Role-based authentication for librarians and customers using custom permissions.
5.	Serializers:
o	Nested serializers for the Book model to include related Author details.
6.	Views:
o	Implemented various views for user login, signup, book details, book requests, and managing requests.
o	API viewsets for Book, Author, BookShelf, and History.
7.	Background Process:
o	Celery task to send email notifications reminding users of the due date for returning borrowed books.

