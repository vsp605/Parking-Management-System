# Database Setup Guide for Parking Management System

## 🚨 Issue Fixed
The main issue was a database name mismatch:
- `app.py` was trying to connect to `parking_management_system`
- `database_setup.sql` creates `parking_system1`
- **Fixed**: Updated `app.py` to use `parking_system1`

## 📋 Prerequisites
1. MySQL Server installed and running
2. Python 3.7+ installed
3. Required Python packages installed

## 🔧 Step-by-Step Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MySQL Server
Make sure MySQL server is running on your system.

### 3. Create Database and Tables
Run the database setup script in MySQL:

**Option A: Using MySQL Command Line**
```bash
mysql -u root -p < database_setup.sql
```

**Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open `database_setup.sql` file
4. Execute the entire script

### 4. Test Database Connection
```bash
python test_db_connection.py
```

### 5. Run the Application
```bash
python app.py
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. "Access denied for user 'root'@'localhost'"
**Solution**: Check your MySQL password
- Update the password in `app.py` line 21
- Or set environment variable: `MYSQL_PASSWORD=your_password`

#### 2. "Unknown database 'parking_system1'"
**Solution**: Database doesn't exist
- Run: `mysql -u root -p < database_setup.sql`
- Or manually create: `CREATE DATABASE parking_system1;`

#### 3. "Can't connect to MySQL server"
**Solution**: MySQL server not running
- Start MySQL service
- Check if MySQL is running on port 3306

#### 4. "ModuleNotFoundError: No module named 'flask_mysqldb'"
**Solution**: Install missing packages
```bash
pip install -r requirements.txt
```

### Environment Variables (Optional)
You can set these environment variables to override defaults:
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=parking_system1
export MYSQL_PORT=3306
```

## 📊 Database Structure
The system creates these tables:
- `users` - User accounts
- `admins` - Admin accounts  
- `ParkingSlot` - Parking slots
- `payments` - Payment records
- `notifications` - System notifications
- `features` - Feature descriptions
- `guidelines` - Parking guidelines

## 🎯 Default Credentials
- **Admin**: admin@parking.com / admin123
- **User**: john@example.com / user123

## ✅ Verification
After setup, you should see:
1. "✅ Database connection successful!" when running test script
2. Flask app starts without database errors
3. Can access http://localhost:5000

## 🆘 Still Having Issues?
1. Check MySQL error logs
2. Verify MySQL user permissions
3. Ensure all tables were created successfully
4. Try connecting with MySQL Workbench first
