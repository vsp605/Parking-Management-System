#!/usr/bin/env python3
"""
Database Connection Test Script
Run this script to test your MySQL database connection before running the main app.
"""

import os
import sys

try:
    import pymysql
    from flask import Flask
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install pymysql flask")
    sys.exit(1)

def test_database_connection():
    """Test the database connection with the same configuration as app.py"""
    
    app = Flask(__name__)
    
    # Database config
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'kane@22*')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'parking_system1')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    
    print("🔧 Testing database connection...")
    print(f"Host: {app.config['MYSQL_HOST']}")
    print(f"User: {app.config['MYSQL_USER']}")
    print(f"Database: {app.config['MYSQL_DB']}")
    print(f"Port: {app.config['MYSQL_PORT']}")
    print("-" * 50)
    
    try:
        # Connect using PyMySQL
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )
        
        with connection.cursor() as cur:
            # Test query
            cur.execute("SELECT 1")
            result = cur.fetchone()
            if result and result[0] == 1:
                print("✅ Database connection successful!")
                
                # Check tables
                cur.execute("SHOW TABLES")
                tables = cur.fetchall()
                
                print(f"📋 Found {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table[0]}")
                
                connection.close()
                return True
            else:
                print("❌ Database connection test failed!")
                connection.close()
                return False
                
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Verify the database 'parking_system1' exists")
        print("3. Check your MySQL credentials")
        print("4. Run: mysql -u root -p < database_setup.sql")
        print("5. Make sure MySQL user has proper permissions")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n🎉 Database is ready! You can now run: python app.py")
    else:
        print("\n💡 Please fix the database connection issues before running the main app.")
        sys.exit(1)
