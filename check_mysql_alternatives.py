#!/usr/bin/env python3
"""
Check for MySQL alternatives and help set up the database
"""

import os
import subprocess
import sys

def check_xampp():
    """Check if XAMPP is installed"""
    print("🔍 Checking for XAMPP installation...")
    
    xampp_paths = [
        r"C:\xampp\mysql\bin\mysql.exe",
        r"C:\xampp\mysql\bin\mysqld.exe",
        r"C:\Program Files\xampp\mysql\bin\mysql.exe",
        r"C:\Program Files (x86)\xampp\mysql\bin\mysql.exe"
    ]
    
    for path in xampp_paths:
        if os.path.exists(path):
            print(f"✅ Found XAMPP MySQL at: {path}")
            return path
    
    print("❌ XAMPP not found")
    return None

def check_mysql_server():
    """Check if MySQL Server is installed"""
    print("🔍 Checking for MySQL Server installation...")
    
    mysql_paths = [
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysql.exe"
    ]
    
    for path in mysql_paths:
        if os.path.exists(path):
            print(f"✅ Found MySQL Server at: {path}")
            return path
    
    print("❌ MySQL Server not found")
    return None

def test_mysql_connection(mysql_path, password=""):
    """Test MySQL connection with given path and password"""
    print(f"🔗 Testing MySQL connection...")
    
    try:
        if password:
            cmd = [mysql_path, '-u', 'root', f'-p{password}', '-e', 'SELECT 1']
        else:
            cmd = [mysql_path, '-u', 'root', '-e', 'SELECT 1']
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ MySQL connection successful!")
            return True
        else:
            print(f"❌ MySQL connection failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MySQL: {e}")
        return False

def setup_with_xampp():
    """Set up database using XAMPP"""
    print("\n🎯 Setting up with XAMPP...")
    
    # Update app.py to use empty password
    print("📝 Updating app.py for XAMPP (no password)...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the password line
        content = content.replace(
            "app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Kane@22*')",
            "app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')"
        )
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated app.py for XAMPP")
        
        # Update setup script
        print("📝 Updating setup script for XAMPP...")
        with open('setup_database.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace(
            "'password': 'Kane@22*',",
            "'password': '',"
        )
        
        with open('setup_database.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated setup script for XAMPP")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating files: {e}")
        return False

def main():
    print("🚀 MySQL Installation Checker")
    print("=" * 50)
    
    # Check for XAMPP
    xampp_path = check_xampp()
    
    # Check for MySQL Server
    mysql_server_path = check_mysql_server()
    
    if not xampp_path and not mysql_server_path:
        print("\n❌ No MySQL installation found!")
        print("\n💡 Solutions:")
        print("1. Install XAMPP (recommended for beginners):")
        print("   - Download from: https://www.apachefriends.org/download.html")
        print("   - Install and start MySQL from XAMPP Control Panel")
        print("\n2. Install MySQL Server:")
        print("   - Download from: https://dev.mysql.com/downloads/installer/")
        print("   - Set root password to: Kane@22*")
        return
    
    # Test connections
    if xampp_path:
        print(f"\n🔧 Testing XAMPP MySQL connection...")
        if test_mysql_connection(xampp_path, ""):  # XAMPP has no password by default
            print("\n🎉 XAMPP MySQL is working!")
            if setup_with_xampp():
                print("\n📋 Next steps:")
                print("1. Make sure XAMPP MySQL is running")
                print("2. Run: python setup_database.py")
                print("3. Run: python test_db_connection.py")
                print("4. Run: python app.py")
                print("\n🔗 Admin login: http://localhost:5000/admin_login")
                print("   Email: admin@parking.com")
                print("   Password: admin123")
            return
    
    if mysql_server_path:
        print(f"\n🔧 Testing MySQL Server connection...")
        if test_mysql_connection(mysql_server_path, "Kane@22*"):
            print("\n🎉 MySQL Server is working!")
            print("\n📋 Next steps:")
            print("1. Run: python setup_database.py")
            print("2. Run: python test_db_connection.py")
            print("3. Run: python app.py")
            print("\n🔗 Admin login: http://localhost:5000/admin_login")
            print("   Email: admin@parking.com")
            print("   Password: admin123")
            return
    
    print("\n❌ Neither MySQL installation is working properly!")
    print("\n💡 Troubleshooting:")
    print("1. For XAMPP: Start MySQL in XAMPP Control Panel")
    print("2. For MySQL Server: Start MySQL service")
    print("3. Check if MySQL is running on port 3306")

if __name__ == "__main__":
    main()
