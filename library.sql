-- ============================================================
-- DIGITAL LIBRARY MANAGEMENT SYSTEM 
-- ============================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- ============================================================
-- Create Users Table (Admin + Students)
-- ============================================================
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user'
);

-- ============================================================
-- Create Categories Table
-- ============================================================
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================================
-- Create Books Table
-- ============================================================
DROP TABLE IF EXISTS books;
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(150) NOT NULL,
    category_id INT NOT NULL,
    available_copies INT DEFAULT 1,
    total_copies INT DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- ============================================================
-- Create Borrow Records Table
-- ============================================================
DROP TABLE IF EXISTS borrow_records;
CREATE TABLE borrow_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE,
    due_date DATE,
    return_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- ============================================================
-- Insert Categories
-- ============================================================
INSERT INTO categories (name) VALUES
('Math'), ('Linux'), ('Operating_System'), ('Python'),
('AI'), ('Database'), ('Networking');

-- ============================================================
--Insert Books Data
-- ============================================================
INSERT INTO books (title, author, category_id, available_copies, total_copies) VALUES
('Linear Algebra and Its Applications', 'Gilbert Strang', 1, 5, 10),
('How Linux Works', 'Brian Ward', 2, 6, 10),
('Operating System Concepts', 'Silberschatz', 3, 8, 10),
('Fluent Python', 'Luciano Ramalho', 4, 5, 10),
('Deep Learning with Python', 'Francois Chollet', 5, 7, 10),
('Database System Concepts', 'Abraham Silberschatz', 6, 9, 10),
('Computer Networking: A Top-Down Approach', 'James F. Kurose', 7, 10, 10),
('Python Crash Course', 'Eric Matthes', 4, 8, 10),
('Artificial Intelligence: A Modern Approach', 'Stuart Russell', 5, 6, 10),
('Linux Bible', 'Christopher Negus', 2, 4, 10);

-- ============================================================
-- Insert Admins
-- ============================================================
INSERT INTO users (username, email, password, role) VALUES
('Admin_Raj', 'rajesh.admin@libmail.com', 'admin123', 'admin'),
('Admin_Priya', 'priya.admin@libmail.com', 'admin123', 'admin'),
('Admin_Vikram', 'vikram.admin@libmail.com', 'admin123', 'admin');

-- ============================================================
-- Insert 20 Random Students
-- ============================================================
INSERT INTO users (username, email, password, role) VALUES
('Nitin', 'nitin.kandwal@college.com', 'user123', 'user'),
('Aditya', 'aditya.sharma@college.com', 'user123', 'user'),
('Kavita', 'kavita.nair@college.com', 'user123', 'user'),
('Manoj', 'manoj.gupta@college.com', 'user123', 'user'),
('Sneha', 'sneha.reddy@college.com', 'user123', 'user'),
('Ravi', 'ravi.desai@college.com', 'user123', 'user'),
('Amit', 'amit.malhotra@college.com', 'user123', 'user'),
('Priya', 'priya.singh@college.com', 'user123', 'user'),
('Suresh', 'suresh.patel@college.com', 'user123', 'user'),
('Neha', 'neha.joshi@college.com', 'user123', 'user'),
('Anjali', 'anjali.sharma@college.com', 'user123', 'user'),
('Rohit', 'rohit.verma@college.com', 'user123', 'user'),
('Meena', 'meena.kulkarni@college.com', 'user123', 'user'),
('Karan', 'karan.mehta@college.com', 'user123', 'user'),
('Pooja', 'pooja.patel@college.com', 'user123', 'user'),
('Akash', 'akash.bansal@college.com', 'user123', 'user'),
('Divya', 'divya.nair@college.com', 'user123', 'user'),
('Varun', 'varun.singh@college.com', 'user123', 'user'),
('Rina', 'rina.das@college.com', 'user123', 'user'),
('Vikas', 'vikas.menon@college.com', 'user123', 'user');

-- ============================================================
--Create a View for Easy Book Display
-- ============================================================
CREATE OR REPLACE VIEW book_view AS
SELECT 
    b.id, 
    b.title, 
    b.author, 
    c.name AS category, 
    b.available_copies, 
    b.total_copies
FROM books b
JOIN categories c ON b.category_id = c.id;

-- ============================================================
-- Create a View for Admin Borrow Report
-- ============================================================
CREATE OR REPLACE VIEW borrow_report_view AS
SELECT 
    u.username AS student_name,
    u.email AS student_email,
    b.title AS book_title,
    br.borrow_date,
    br.due_date,
    br.return_date
FROM borrow_records br
JOIN users u ON br.user_id = u.id
JOIN books b ON br.book_id = b.id;

-- ============================================================
-- Create Trigger - Update Book Copies When Returned
-- ============================================================
DELIMITER //
CREATE TRIGGER update_book_copies
AFTER UPDATE ON borrow_records
FOR EACH ROW
BEGIN
    IF NEW.return_date IS NOT NULL THEN
        UPDATE books
        SET available_copies = available_copies + 1
        WHERE id = NEW.book_id;
    END IF;
END;
//
DELIMITER ;

-- ============================================================
--Create Stored Procedure for Searching Books
-- ============================================================
DELIMITER //
CREATE PROCEDURE search_books(IN keyword VARCHAR(100))
BEGIN
    SELECT 
        b.id, 
        b.title, 
        b.author, 
        c.name AS category, 
        b.available_copies
    FROM books b
    JOIN categories c ON b.category_id = c.id
    WHERE b.title LIKE CONCAT('%', keyword, '%')
       OR b.author LIKE CONCAT('%', keyword, '%')
       OR c.name LIKE CONCAT('%', keyword, '%');
END;
//
DELIMITER ;

-- ============================================================
-- TEST QUERIES (Optional)
-- ============================================================

-- Show all admins
SELECT * FROM users WHERE role='admin';

-- Show all students
SELECT * FROM users WHERE role='user';

-- Show all books with category
SELECT * FROM book_view;

-- Test stored procedure
CALL search_books('Python');

-- View admin borrow report
SELECT * FROM borrow_report_view;

