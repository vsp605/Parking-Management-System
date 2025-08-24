Parking System Flask Application
A web-based parking management system built with Flask, MySQL, and Python. The application supports user and admin roles, enabling slot booking, payments, and management of parking spaces with user-friendly dashboards.

Features
User Registration & Login: Secure authentication, profile picture upload, password hashing.

Admin Registration & Login: Separate access for admins, dashboard, and management tools.

Slot Management: Add, edit, and delete parking slots; track availability and bookings.

Booking: Users can reserve available slots and view location-based options.

Payment & Billing: Dynamic payment calculation (by vehicle type/hours), bills in HTML and PDF.

Notifications: Admins can create notifications for users.

Features & Guidelines: System features and guidelines can be added and updated by admins.

Session Management & Security: Sessions, upload restrictions, allowed file types, and error logging.

Extensive Logging: Debug and error logs for troubleshooting.

Technology Stack
Backend: Python, Flask, Flask-MySQLdb, Werkzeug

Database: MySQL (parking_system1)

Frontend: Flask templates (HTML, CSS, JS)

PDF Generation: Optional via pdfkit + wkhtmltopdf

Getting Started
Prerequisites
Python 3.x

MySQL Server

pip (Python package installer)

Installation
Clone the repository:

bash
git clone https://github.com/your-username/parking-system-flask.git
cd parking-system-flask
Install Python dependencies:

bash
pip install flask flask-mysqldb werkzeug pdfkit
Create MySQL Database:

Start MySQL server.

Run SQL scripts to create database and tables (see database_setup.sql if provided).

Example:

sql
CREATE DATABASE parking_system1;
USE parking_system1;
-- Create necessary tables as per app.py requirements
Configure environment variables (optional):

Copy .env.example to .env and set:

text
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=parking_system1
SECRET_KEY=your-secret-key
Running the App
bash
python app.py
The app runs at http://localhost:5000/ by default.

Folder Structure
text
.
├── app.py
├── requirements.txt
├── README.md
├── static/
│   └── uploads/
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── admin_register.html
│   ├── admin_dashboard.html
│   ├── admin_manage_slots.html
│   ├── features.html
│   ├── guidelines.html
│   ├── Slots.html
│   ├── Payment.html
│   ├── Guidelines.html
│   ├── Features.html
│   ├── Bill.html
│   └── ...etc.
Usage
User: Register, login, view slots, book a slot, pay, and download bill.

Admin: Register/login, manage slots and payments, add features/guidelines, view dashboard.

Security Note
For production, move all sensitive config values to environment variables.

Hash admin passwords (not just user passwords).

Use HTTPS and strong secret keys.

