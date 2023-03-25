# SecurityBaseProject

## Installation Instructions:

- Clone the repository to your local machine.
- Create a virtual environment and activate it.
- Navigate to the project directory.
- A secret key can be provided via the environment variable “SECRET_KEY” in settings.py.
- For the DATABASES variable you can use the default one provided by Django
-- 'ENGINE': 'django.db.backends.sqlite3' and 'NAME': 'db.sqlite3'
- Run the command "python manage.py migrate" to create the database tables.
- Run the command "python manage.py runserver" to start the server.
- Navigate to http://localhost:8000/ to view the application.

## Usage
- You can create a new account by navigating to http://localhost:8000/account/signup
