# MySQL Installation and Setup Guide for Windows

## 🚨 Current Issue
Your system doesn't have MySQL installed or configured properly. Here's how to fix it:

## 📋 Step 1: Install MySQL

### Option A: Install MySQL Server (Recommended)
1. **Download MySQL Installer**:
   - Go to: https://dev.mysql.com/downloads/installer/
   - Download "MySQL Installer for Windows"
   - Choose the larger file (~450MB) that includes all products

2. **Run the Installer**:
   - Run the downloaded `.msi` file
   - Choose "Developer Default" or "Server only"
   - Follow the installation wizard

3. **Set Root Password**:
   - When prompted, set the root password to: `Kane@22*`
   - **IMPORTANT**: Remember this password!

### Option B: Install XAMPP (Easier Alternative)
1. **Download XAMPP**:
   - Go to: https://www.apachefriends.org/download.html
   - Download XAMPP for Windows
   - Install it (includes MySQL, Apache, PHP)

2. **Start MySQL**:
   - Open XAMPP Control Panel
   - Click "Start" next to MySQL
   - The default root password is empty (blank)

## 📋 Step 2: Verify MySQL Installation

### Check if MySQL is installed:
```bash
mysql --version
```

### If MySQL is not in PATH, try these locations:
- `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`
- `C:\xampp\mysql\bin\mysql.exe`

## 📋 Step 3: Start MySQL Service

### If using MySQL Server:
```bash
# Start MySQL service
net start mysql

# Or use Services app:
# 1. Press Win+R, type "services.msc"
# 2. Find "MySQL" service
# 3. Right-click → Start
```

### If using XAMPP:
- Open XAMPP Control Panel
- Click "Start" next to MySQL

## 📋 Step 4: Test MySQL Connection

### Test with default settings:
```bash
mysql -u root -p
# Enter password when prompted
```

### If password is blank (XAMPP default):
```bash
mysql -u root
```

## 📋 Step 5: Update App Configuration

### If using XAMPP (no password):
Edit `app.py` and change line 21:
```python
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')  # Empty password
```

### If using MySQL Server with different password:
Edit `app.py` and change line 21:
```python
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'your_actual_password')
```

## 📋 Step 6: Set Up Database

### Run the setup script:
```bash
python setup_database.py
```

### Or manually create database:
```bash
mysql -u root -p
# Enter your password

# Then run these commands:
CREATE DATABASE parking_system1;
USE parking_system1;
# Then run the contents of database_setup.sql
```

## 📋 Step 7: Test Everything

### Test database connection:
```bash
python test_db_connection.py
```

### Run the application:
```bash
python app.py
```

## 🔍 Troubleshooting

### "Access denied for user 'root'@'localhost'"
**Solutions**:
1. Check if password is correct
2. Try connecting without password: `mysql -u root`
3. Reset MySQL root password if needed

### "MySQL command not found"
**Solutions**:
1. MySQL is not installed - follow installation steps above
2. MySQL is not in PATH - add MySQL bin directory to PATH
3. Use full path to mysql.exe

### "Can't connect to MySQL server"
**Solutions**:
1. Start MySQL service
2. Check if MySQL is running on port 3306
3. Check firewall settings

### "Service not found"
**Solutions**:
1. MySQL service not installed - reinstall MySQL
2. Service name might be different - check Services app

## 🎯 Quick Fix for XAMPP Users

If you're using XAMPP, here's the quickest solution:

1. **Install XAMPP** (if not already installed)
2. **Start MySQL** in XAMPP Control Panel
3. **Update app.py** password to empty string:
   ```python
   app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
   ```
4. **Run setup**:
   ```bash
   python setup_database.py
   ```
5. **Test and run**:
   ```bash
   python test_db_connection.py
   python app.py
   ```

## 📞 Admin Login Information

Once everything is set up, you can access the admin panel at:
- **URL**: http://localhost:5000/admin_login
- **Email**: admin@parking.com
- **Password**: admin123

## ✅ Success Indicators

You'll know everything is working when:
1. `python test_db_connection.py` shows "✅ Database connection successful!"
2. `python app.py` starts without database errors
3. You can access http://localhost:5000
4. Admin login works at http://localhost:5000/admin_login
