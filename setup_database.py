#!/usr/bin/env python3
"""
Database Setup Script
This script will create the database and tables using Python instead of MySQL command line.
"""

import os
import sys

def setup_database():
    """Set up the database using Python MySQL connector"""
    
    print("🚀 Setting up Parking Management System Database...")
    
    try:
        import mysql.connector
        from mysql.connector import Error
    except ImportError:
        print("❌ mysql-connector-python not installed!")
        print("Please install it: pip install mysql-connector-python")
        return False
    
    # Database configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'kane@22*',
        'port': 3306
    }
    
    try:
        # Connect to MySQL server (without specifying database)
        print("🔗 Connecting to MySQL server...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if not exists
            print("📦 Creating database 'parking_system1'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS parking_system1")
            print("✅ Database created successfully!")
            
            # Use the database
            cursor.execute("USE parking_system1")
            
            # Create tables
            print("📋 Creating tables...")
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone VARCHAR(15),
                    profile_picture VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Admins table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone VARCHAR(15),
                    role VARCHAR(20) DEFAULT 'admin',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # ParkingSlot table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ParkingSlot (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    location VARCHAR(100) NOT NULL,
                    slot_number INT NOT NULL,
                    status ENUM('available', 'booked', 'maintenance') DEFAULT 'available',
                    user_id INT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                    UNIQUE KEY unique_slot_location (location, slot_number)
                )
            """)
            
            # Payments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    plot_no VARCHAR(20) NOT NULL,
                    vehicle_no VARCHAR(20) NOT NULL,
                    vehicle_type ENUM('2wheeler', '4wheeler') NOT NULL,
                    hours INT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    payment_type ENUM('cash', 'card', 'online') NOT NULL,
                    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'completed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Notifications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    type ENUM('info', 'warning', 'success', 'error') DEFAULT 'info',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Features table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS features (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT NOT NULL,
                    icon VARCHAR(50),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Guidelines table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS guidelines (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    category VARCHAR(50),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            print("✅ All tables created successfully!")
            
            # Insert sample data
            print("📝 Inserting sample data...")
            
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM notifications")
            if cursor.fetchone()[0] == 0:
                # Insert sample notifications
                notifications_data = [
                    ('Welcome to Parking Management System', 'Thank you for registering with our parking management system. Enjoy hassle-free parking!', 'success'),
                    ('New Feature Available', 'We have introduced online payment options for your convenience.', 'info'),
                    ('Maintenance Notice', 'Parking slots 5-8 will be under maintenance on Sunday. Please plan accordingly.', 'warning'),
                    ('Holiday Schedule', 'Parking rates will be revised during upcoming holidays. Check our pricing page for details.', 'info')
                ]
                
                cursor.executemany("""
                    INSERT INTO notifications (title, message, type) VALUES (%s, %s, %s)
                """, notifications_data)
                
                # Insert sample features
                features_data = [
                    ('Easy Booking', 'Book your parking slot in just a few clicks with our user-friendly interface.', '🚗'),
                    ('Real-time Availability', 'Check slot availability in real-time and avoid waiting in queues.', '⏰'),
                    ('Secure Payments', 'Multiple payment options with secure transaction processing.', '💳'),
                    ('24/7 Support', 'Round-the-clock customer support for all your parking needs.', '📞'),
                    ('Mobile App', 'Access parking services on the go with our mobile application.', '📱'),
                    ('Digital Receipts', 'Get digital receipts instantly after payment completion.', '🧾')
                ]
                
                cursor.executemany("""
                    INSERT INTO features (title, description, icon) VALUES (%s, %s, %s)
                """, features_data)
                
                # Insert sample guidelines
                guidelines_data = [
                    ('General Parking Rules', '1. Park only in designated slots\n2. Follow traffic rules\n3. Keep your vehicle locked\n4. Do not block other vehicles', 'general'),
                    ('Payment Guidelines', '1. Payment must be completed before parking\n2. Keep payment receipt for verification\n3. Multiple payment methods accepted\n4. Refunds processed within 24 hours', 'payment'),
                    ('Safety Guidelines', '1. Do not leave valuables in your vehicle\n2. Report any suspicious activity\n3. Follow emergency exit signs\n4. Keep emergency contacts handy', 'safety'),
                    ('Vehicle Guidelines', '1. Ensure your vehicle is in good condition\n2. Follow size restrictions for slots\n3. Do not park oversized vehicles in regular slots\n4. Report any vehicle damage immediately', 'vehicle')
                ]
                
                cursor.executemany("""
                    INSERT INTO guidelines (title, content, category) VALUES (%s, %s, %s)
                """, guidelines_data)
                
                # Insert sample parking slots
                slot_data = []
                for location in ['mall', 'office', 'hospital']:
                    for slot_num in range(1, 11):
                        slot_data.append((location, slot_num, 'available'))
                
                cursor.executemany("""
                    INSERT INTO ParkingSlot (location, slot_number, status) VALUES (%s, %s, %s)
                """, slot_data)
                
                print("✅ Sample data inserted successfully!")
            else:
                print("ℹ️ Sample data already exists, skipping...")
            
            # Commit changes
            connection.commit()
            
            # Show table counts
            print("\n📊 Database Summary:")
            tables = ['users', 'admins', 'ParkingSlot', 'payments', 'notifications', 'features', 'guidelines']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   - {table}: {count} records")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Database setup completed successfully!")
            print("You can now run: python app.py")
            return True
            
    except Error as e:
        print(f"❌ Database error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check if the password 'Kane@22*' is correct")
        print("3. Verify MySQL is installed and accessible")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    if not success:
        sys.exit(1) 