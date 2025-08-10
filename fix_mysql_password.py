#!/usr/bin/env python3
"""
MySQL Password Fix Script
This script helps you fix MySQL password issues
"""

import os
import subprocess
import sys

def try_common_passwords():
    """Try common MySQL passwords"""
    print("🔍 Trying common MySQL passwords...")
    
    mysql_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    
    common_passwords = [
        "",  # Empty password
        "root",
        "password",
        "admin",
        "123456",
        "mysql",
        "Kane@22*",  # Original password
        "kane@22*",  # Lowercase
        "Kane22",    # Without special chars
        "kane22"     # Lowercase without special chars
    ]
    
    for password in common_passwords:
        print(f"   Trying password: {'(empty)' if password == '' else password}")
        
        try:
            if password:
                cmd = [mysql_path, '-u', 'root', f'-p{password}', '-e', 'SELECT 1']
            else:
                cmd = [mysql_path, '-u', 'root', '-e', 'SELECT 1']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print(f"✅ SUCCESS! Password is: {'(empty)' if password == '' else password}")
                return password
                
        except Exception as e:
            continue
    
    print("❌ None of the common passwords worked")
    return None

def update_app_config(password):
    """Update app.py with the correct password"""
    print(f"📝 Updating app.py with password: {'(empty)' if password == '' else password}")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the password line
        if password:
            new_password_line = f"app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '{password}')"
        else:
            new_password_line = "app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')"
        
        content = content.replace(
            "app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Kane@22*')",
            new_password_line
        )
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated app.py")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        return False

def update_setup_script(password):
    """Update setup_database.py with the correct password"""
    print(f"📝 Updating setup_database.py with password: {'(empty)' if password == '' else password}")
    
    try:
        with open('setup_database.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the password line
        if password:
            new_password_line = f"'password': '{password}',"
        else:
            new_password_line = "'password': '',"
        
        content = content.replace(
            "'password': 'Kane@22*',",
            new_password_line
        )
        
        with open('setup_database.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated setup_database.py")
        return True
        
    except Exception as e:
        print(f"❌ Error updating setup_database.py: {e}")
        return False

def reset_mysql_password():
    """Instructions to reset MySQL password"""
    print("\n🔧 MySQL Password Reset Instructions:")
    print("=" * 50)
    print("1. Stop MySQL service:")
    print("   - Press Win+R, type 'services.msc'")
    print("   - Find 'MySQL80' or 'MySQL' service")
    print("   - Right-click → Stop")
    print("\n2. Start MySQL in safe mode:")
    print("   - Open Command Prompt as Administrator")
    print("   - Run: cd 'C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin'")
    print("   - Run: mysqld --skip-grant-tables --user=mysql")
    print("\n3. In another Command Prompt:")
    print("   - Run: mysql -u root")
    print("   - Run: USE mysql;")
    print("   - Run: ALTER USER 'root'@'localhost' IDENTIFIED BY 'Kane@22*';")
    print("   - Run: FLUSH PRIVILEGES;")
    print("   - Run: EXIT;")
    print("\n4. Restart MySQL service normally")
    print("\n5. Test with: mysql -u root -p")
    print("   Enter password: Kane@22*")

def main():
    print("🔐 MySQL Password Fix Tool")
    print("=" * 50)
    
    # Try common passwords
    working_password = try_common_passwords()
    
    if working_password is not None:
        print(f"\n🎉 Found working password!")
        
        # Update configuration files
        if update_app_config(working_password) and update_setup_script(working_password):
            print("\n✅ Configuration updated successfully!")
            print("\n📋 Next steps:")
            print("1. Run: python setup_database.py")
            print("2. Run: python test_db_connection.py")
            print("3. Run: python app.py")
            print("\n🔗 Admin login: http://localhost:5000/admin_login")
            print("   Email: admin@parking.com")
            print("   Password: admin123")
        else:
            print("\n❌ Failed to update configuration files")
    else:
        print("\n❌ Could not find working password")
        print("\n💡 Options:")
        print("1. Reset MySQL password (see instructions below)")
        print("2. Install XAMPP (easier alternative)")
        print("3. Contact your system administrator")
        
        reset_mysql_password()

if __name__ == "__main__":
    main()
