#!/usr/bin/env python3
"""
Database Diagnostic Script
This script will help identify the exact database connection issue.
"""

import os
import sys
import subprocess

def check_mysql_service():
    """Check if MySQL service is running"""
    print("🔍 Checking MySQL service status...")
    
    try:
        # Try to connect to MySQL without specifying a database
        result = subprocess.run(['mysql', '-u', 'root', '-pKane@22*', '-e', 'SELECT 1'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ MySQL service is running and accessible")
            return True
        else:
            print(f"❌ MySQL service error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ MySQL command not found. Is MySQL installed?")
        return False
    except subprocess.TimeoutExpired:
        print("❌ MySQL connection timeout. Service might not be running.")
        return False
    except Exception as e:
        print(f"❌ Error checking MySQL service: {e}")
        return False

def check_database_exists():
    """Check if the parking_system1 database exists"""
    print("\n🔍 Checking if database 'parking_system1' exists...")
    
    try:
        result = subprocess.run([
            'mysql', '-u', 'root', '-pKane@22*', 
            '-e', 'SHOW DATABASES LIKE "parking_system1"'
        ], capture_output=True, text=True, timeout=10)
        
        if 'parking_system1' in result.stdout:
            print("✅ Database 'parking_system1' exists")
            return True
        else:
            print("❌ Database 'parking_system1' does not exist")
            return False
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def check_tables():
    """Check if required tables exist"""
    print("\n🔍 Checking if required tables exist...")
    
    try:
        result = subprocess.run([
            'mysql', '-u', 'root', '-pKane@22*', 'parking_system1',
            '-e', 'SHOW TABLES'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            tables = result.stdout.strip().split('\n')[1:]  # Skip header
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                if table.strip():
                    print(f"   - {table.strip()}")
            return True
        else:
            print(f"❌ Error checking tables: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def test_flask_connection():
    """Test Flask-MySQLdb connection"""
    print("\n🔍 Testing Flask-MySQLdb connection...")
    
    try:
        from flask import Flask
        from flask_mysqldb import MySQL
        
        app = Flask(__name__)
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'Kane@22*'
        app.config['MYSQL_DB'] = 'parking_system1'
        app.config['MYSQL_PORT'] = 3306
        
        mysql = MySQL(app)
        
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            result = cur.fetchone()
            cur.close()
            
            if result and result[0] == 1:
                print("✅ Flask-MySQLdb connection successful!")
                return True
            else:
                print("❌ Flask-MySQLdb connection failed")
                return False
                
    except Exception as e:
        print(f"❌ Flask-MySQLdb connection error: {e}")
        return False

def main():
    print("🚀 Database Diagnostic Tool")
    print("=" * 50)
    
    # Check MySQL service
    mysql_running = check_mysql_service()
    
    if not mysql_running:
        print("\n💡 Solutions:")
        print("1. Start MySQL service:")
        print("   - Windows: net start mysql")
        print("   - Linux/Mac: sudo service mysql start")
        print("2. Check if MySQL is installed")
        print("3. Verify MySQL is running on port 3306")
        return
    
    # Check database exists
    db_exists = check_database_exists()
    
    if not db_exists:
        print("\n💡 Solutions:")
        print("1. Create the database by running:")
        print("   mysql -u root -p < database_setup.sql")
        print("2. Or manually create:")
        print("   mysql -u root -p")
        print("   CREATE DATABASE parking_system1;")
        return
    
    # Check tables
    tables_exist = check_tables()
    
    if not tables_exist:
        print("\n💡 Solutions:")
        print("1. Run the database setup script:")
        print("   mysql -u root -p < database_setup.sql")
        return
    
    # Test Flask connection
    flask_works = test_flask_connection()
    
    if flask_works:
        print("\n🎉 All checks passed! Your database is ready.")
        print("You can now run: python app.py")
    else:
        print("\n💡 Flask connection failed. Check:")
        print("1. Flask-MySQLdb installation: pip install Flask-MySQLdb")
        print("2. MySQL user permissions")
        print("3. Database configuration in app.py")

if __name__ == "__main__":
    main()


