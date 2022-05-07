# CRM
This is a relational database Customer Relationship Manager, which was built using the flask-sqlalchemy ORM. The CRM holds three relational tables, allows for creation of new clients and appointments on any day of the year, deletion of appointments or clients, viewing of schedule for any date range within the year, and retrieval of client appointment history. All of these routes are accessible by the home page user interface, or by entry in the URL bar.


Installation Instructions:

clone repository

pipenv install pandas numpy python-dotenv flask flask-sqlalchemy datetime

pipenv shell

export FLASK_APP=littlecrm

flask run


Routes:

/load_db - initialize the calendar, required before first use of the app and after each refresh

/schedule_appointment - create appointments for existing clients

/view_planner - view all schedulings for a date or date range

/create_client - create a new client in the database

/delete_client - remove client from database

/delete_appointment - remove appointment from database

/client_appointments - view past and future appointments for a client

/check - view the occupancy of the Day, Client and Appointment tables, as well as appointment ID's for existing appointments

/refresh - wipe all Day, Client and Appointment objects from database

