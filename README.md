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
•	User: Custom user model extending AbstractUser with fields is_librarian(superuser) and is_customer.
•	Author: Model to store author details.
•	BookShelf: Model to store bookshelf location.
•	Book: Model to store book details, including a foreign key to Author and BookShelf.
•	History: Model to track the history of borrowed books.
•	BookRequest: Model to handle book requests and their statuses.
2.	Signals:
•	Automatically creates or updates an entry in the History model whenever a BookRequest status is changed to 'approved' or 'returned'.
3.	Middleware:
•	EncryptionMiddleware: Encrypts user emails based on a setting.
•	LoginRequiredMiddleware: Redirects non-authenticated users to the login page.
4.	Authentication:
•	Role-based authentication for librarians and customers using custom permissions.
5.	Serializers:
•	Nested serializers for the Book model to include related Author details.
6.	Views:
•	Implemented various views for user login, signup, book details, book requests, and managing requests.
•	API viewsets for Book, Author, BookShelf, and History.
7.	Background Process:
•	Celery task to send email notifications reminding users of the due date for returning borrowed books.




Instructions to Run the Project
Clone the Repository:


git clone <repository_url>
cd <repository_directory>
Create and Activate a Virtual Environment:


python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install Dependencies:

pip install -r requirements.txt
Setup Django Project:
Make Migrations:

python manage.py makemigrations
python manage.py migrate
Create Superuser
python manage.py createsuperuser

Collect Static Files:
python manage.py collectstatic


Run the Development Server:
python manage.py runserver


Setup Celery:
Run Celery Worker:

celery -A library_project worker --loglevel=info
Access the Application:

Open  browser and go to http://127.0.0.1:8000/ to access the home page.
Use the Django admin interface at http://127.0.0.1:8000/admin/ to manage  models.
