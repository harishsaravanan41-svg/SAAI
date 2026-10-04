-- ====================================================
-- SACAS College Database Schema
-- ====================================================

-- 1. Departments
CREATE TABLE IF NOT EXISTS departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    url VARCHAR(500)
);

-- 2. Clubs
CREATE TABLE IF NOT EXISTS clubs (
    club_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    parent_body VARCHAR(255)
);

-- 3. Staff
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    qualification VARCHAR(255),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
);

-- 4. Events
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT,
    club_id INT,
    title VARCHAR(500) NOT NULL,
    event_date DATE NOT NULL,
    venue VARCHAR(255),
    description TEXT,
    url VARCHAR(500),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE SET NULL
);

-- 5. Student Result
CREATE TABLE IF NOT EXISTS student_result (
    s_no INT,
    register_number BIGINT PRIMARY KEY,
    department_id INT,
    name VARCHAR(255) NOT NULL,
    dob DATE,
    python_practical INT,
    tamil INT,
    english INT,
    python INT,
    office_automation INT,
    naan_mudhalvan INT,
    main_total INT,
    percentage DECIMAL(5,2),
    rank INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);

-- 6. Users (Authentication & Identity)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student' NOT NULL,
    register_number BIGINT UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE
);
