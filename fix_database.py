#!/usr/bin/env python3
"""
Quick Fix for Database Connection Issues
Run this script to fix common database connection problems.
"""

import os
import sys

def check_mysql_installation():
    """Check if MySQL is installed and running"""
    print("🔍 Checking MySQL installation...")
    
    # Check if MySQL service is running (Windows)
    try:
        import subprocess
        result = subprocess.run(['sc', 'query', 'mysql'], capture_output=True, text=True)
        if 'RUNNING' in result.stdout:
            print("✅ MySQL service is running")
            return True
        else:
            print("❌ MySQL service is not running")
            return False
    except:
        print("⚠️ Could not check MySQL service status")
        return True  # Assume it's running

def create_env_file():
    """Create .env file with proper configuration"""
    print("📝 Creating .env file...")
    
    env_content = """# Parking Management System Environment Variables
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Kane@22*
MYSQL_DB=parking_system1
SECRET_KEY=f894cb67a8c0b040dc8243b0864a320f
UPLOAD_FOLDER=static/uploads
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created")

def create_upload_folder():
    """Create upload folder"""
    print("📁 Creating upload folder...")
    
    try:
        os.makedirs('static/uploads', exist_ok=True)
        print("✅ Upload folder created")
    except Exception as e:
        print(f"❌ Failed to create upload folder: {e}")

def main():
    print("🔧 Parking Management System - Database Fix")
    print("=" * 50)
    
    # Check MySQL
    if not check_mysql_installation():
        print("\n💡 To start MySQL service:")
        print("1. Open Command Prompt as Administrator")
        print("2. Run: net start mysql")
        print("3. Or use MySQL Installer to start the service")
        return
    
    # Create .env file
    create_env_file()
    
    # Create upload folder
    create_upload_folder()
    
    print("\n🎯 Next Steps:")
    print("1. Run: python setup_database.py")
    print("2. Run: python app.py")
    print("\n📋 If you still have issues:")
    print("1. Make sure MySQL is running")
    print("2. Check your MySQL password in .env file")
    print("3. Ensure you have proper permissions")

if __name__ == "__main__":
    main() 