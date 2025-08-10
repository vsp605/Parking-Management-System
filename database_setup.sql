-- Parking Management System Database Setup
-- Run this script in MySQL to create all necessary tables

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS parking_system1;
USE parking_system1;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS ParkingSlot;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS features;
DROP TABLE IF EXISTS guidelines;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admins;

-- Create Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    profile_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Admins Table
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    role VARCHAR(20) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Parking Slots Table
CREATE TABLE ParkingSlot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    slot_number INT NOT NULL,
    status ENUM('available', 'booked', 'maintenance') DEFAULT 'available',
    user_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_slot_location (location, slot_number)
);

-- Create Payments Table
CREATE TABLE payments (
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
);

-- Create Notifications Table
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('info', 'warning', 'success', 'error') DEFAULT 'info',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Features Table
CREATE TABLE features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Guidelines Table
CREATE TABLE guidelines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert Sample Admin (password: admin123)
INSERT INTO admins (username, email, password, phone, role) VALUES 
('admin', 'admin@parking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', '+91 98765 43210', 'super_admin');

-- Insert Sample Users (password: user123)
INSERT INTO users (username, email, password, phone) VALUES 
('john_doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', '+91 98765 43211'),
('jane_smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', '+91 98765 43212');

-- Insert Sample Parking Slots
INSERT INTO ParkingSlot (location, slot_number, status) VALUES 
-- Mall Parking
('mall', 1, 'available'),
('mall', 2, 'available'),
('mall', 3, 'available'),
('mall', 4, 'available'),
('mall', 5, 'available'),
('mall', 6, 'available'),
('mall', 7, 'available'),
('mall', 8, 'available'),
('mall', 9, 'available'),
('mall', 10, 'available'),

-- Office Parking
('office', 1, 'available'),
('office', 2, 'available'),
('office', 3, 'available'),
('office', 4, 'available'),
('office', 5, 'available'),
('office', 6, 'available'),
('office', 7, 'available'),
('office', 8, 'available'),
('office', 9, 'available'),
('office', 10, 'available'),

-- Hospital Parking
('hospital', 1, 'available'),
('hospital', 2, 'available'),
('hospital', 3, 'available'),
('hospital', 4, 'available'),
('hospital', 5, 'available'),
('hospital', 6, 'available'),
('hospital', 7, 'available'),
('hospital', 8, 'available'),
('hospital', 9, 'available'),
('hospital', 10, 'available');

-- Insert Sample Notifications
INSERT INTO notifications (title, message, type) VALUES 
('Welcome to Parking Management System', 'Thank you for registering with our parking management system. Enjoy hassle-free parking!', 'success'),
('New Feature Available', 'We have introduced online payment options for your convenience.', 'info'),
('Maintenance Notice', 'Parking slots 5-8 will be under maintenance on Sunday. Please plan accordingly.', 'warning'),
('Holiday Schedule', 'Parking rates will be revised during upcoming holidays. Check our pricing page for details.', 'info');

-- Insert Sample Features
INSERT INTO features (title, description, icon) VALUES 
('Easy Booking', 'Book your parking slot in just a few clicks with our user-friendly interface.', '🚗'),
('Real-time Availability', 'Check slot availability in real-time and avoid waiting in queues.', '⏰'),
('Secure Payments', 'Multiple payment options with secure transaction processing.', '💳'),
('24/7 Support', 'Round-the-clock customer support for all your parking needs.', '📞'),
('Mobile App', 'Access parking services on the go with our mobile application.', '📱'),
('Digital Receipts', 'Get digital receipts instantly after payment completion.', '🧾');

-- Insert Sample Guidelines
INSERT INTO guidelines (title, content, category) VALUES 
('General Parking Rules', '1. Park only in designated slots\n2. Follow traffic rules\n3. Keep your vehicle locked\n4. Do not block other vehicles', 'general'),
('Payment Guidelines', '1. Payment must be completed before parking\n2. Keep payment receipt for verification\n3. Multiple payment methods accepted\n4. Refunds processed within 24 hours', 'payment'),
('Safety Guidelines', '1. Do not leave valuables in your vehicle\n2. Report any suspicious activity\n3. Follow emergency exit signs\n4. Keep emergency contacts handy', 'safety'),
('Vehicle Guidelines', '1. Ensure your vehicle is in good condition\n2. Follow size restrictions for slots\n3. Do not park oversized vehicles in regular slots\n4. Report any vehicle damage immediately', 'vehicle');

-- Show all tables
SHOW TABLES;

-- Show sample data
SELECT 'Users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Admins' as table_name, COUNT(*) as count FROM admins
UNION ALL
SELECT 'Parking Slots' as table_name, COUNT(*) as count FROM ParkingSlot
UNION ALL
SELECT 'Notifications' as table_name, COUNT(*) as count FROM notifications
UNION ALL
SELECT 'Features' as table_name, COUNT(*) as count FROM features
UNION ALL
SELECT 'Guidelines' as table_name, COUNT(*) as count FROM guidelines; 