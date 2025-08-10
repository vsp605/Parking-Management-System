# Parking Management System - Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
1. **Install MySQL** if not already installed
2. **Run the database setup script**:
   ```bash
   mysql -u root -p < database_setup.sql
   ```
   Or copy and paste the contents of `database_setup.sql` into your MySQL client.

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=parking_system1
SECRET_KEY=your_secret_key_here
UPLOAD_FOLDER=static/uploads
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📋 Default Login Credentials

### Admin Access
- **Email**: admin@parking.com
- **Password**: admin123

### Sample User Accounts
- **Email**: john@example.com
- **Password**: user123

- **Email**: jane@example.com
- **Password**: user123

## 🗄️ Database Structure

### Tables Created:
1. **users** - Regular user accounts
2. **admins** - Admin user accounts
3. **ParkingSlot** - Parking slot information
4. **payments** - Payment transactions
5. **notifications** - System notifications
6. **features** - System features
7. **guidelines** - Parking guidelines

### Sample Data Included:
- 30 parking slots (10 each for mall, office, hospital)
- 4 sample notifications
- 6 system features
- 4 parking guidelines
- 1 admin account
- 2 sample user accounts

## 🔧 PDF Generation Setup

### Option 1: Install wkhtmltopdf (Recommended)
1. **Windows**: Download from https://wkhtmltopdf.org/downloads.html
2. **Linux**: `sudo apt-get install wkhtmltopdf`
3. **macOS**: `brew install wkhtmltopdf`

### Option 2: Use HTML Fallback
If wkhtmltopdf is not available, the system will automatically fall back to HTML bill generation.

## 🛠️ Troubleshooting

### Common Issues:

1. **MySQL Connection Error**
   - Verify MySQL is running
   - Check database credentials in `.env` file
   - Ensure database `parking_system1` exists

2. **PDF Generation Fails**
   - Install wkhtmltopdf
   - Check file permissions
   - System will fall back to HTML if PDF fails

3. **Template Errors**
   - Ensure all template files are in the `templates/` directory
   - Check for syntax errors in HTML files

4. **Upload Folder Issues**
   - Create `static/uploads/` directory
   - Ensure write permissions

### Logs
Check the console output for detailed error messages and debugging information.

## 📱 Features

### User Features:
- User registration and login
- View available parking slots
- Book parking slots
- Make payments
- Generate bills (PDF/HTML)
- View notifications
- Access features and guidelines

### Admin Features:
- Admin dashboard with statistics
- View all users, slots, and payments
- Add features and guidelines
- Manage system content

### System Features:
- Real-time slot availability
- Automatic amount calculation
- Multiple payment methods
- PDF bill generation
- Responsive design
- Session management

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Admin/user role separation
- Input validation and sanitization
- SQL injection prevention

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs for error messages
3. Verify database connectivity
4. Ensure all dependencies are installed

## 🚀 Deployment

### For Production:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure a reverse proxy (Nginx, Apache)
4. Use environment variables for sensitive data
5. Set up SSL/TLS certificates
6. Configure proper logging 