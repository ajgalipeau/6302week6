-- galipeau ddl.sql
-- This has been refactored to increase flexibility, data integrity, and performance

-- Drop the existing database if it exists
DROP DATABASE IF EXISTS SCHOOL;
CREATE DATABASE IF NOT EXISTS SCHOOL;
USE SCHOOL;

-- Drop and create TEACHER table
DROP TABLE IF EXISTS TEACHER;
CREATE TABLE TEACHER (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for teachers
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email_address VARCHAR(100) NOT NULL UNIQUE -- Ensures unique email addresses
);

-- Drop and create STUDENT table
-- student_grade now refers to the student's level of education (e.g., grade 6, 7, or 8)
DROP TABLE IF EXISTS STUDENT;
CREATE TABLE STUDENT (
    student_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for students
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email_address VARCHAR(100) NOT NULL UNIQUE, -- Ensures unique email addresses
    date_of_birth DATE NULL,
    student_grade INT NOT NULL -- Represents the student's educational grade level (e.g., 6, 7, or 8)
);

-- Drop and create CLASSES table
DROP TABLE IF EXISTS CLASSES;
CREATE TABLE CLASSES (
    class_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for classes
    class_subject VARCHAR(100) NOT NULL, -- Subject name
    teacher_id INT, -- References TEACHER table
    FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id)
        ON DELETE SET NULL ON UPDATE CASCADE -- Maintain teacher-student relationship
);

-- Drop and create STUDENT_CLASSES table to manage student-class relationships
-- class_grade now refers to the grade received in the class (A, B, etc.)
DROP TABLE IF EXISTS STUDENT_CLASSES;
CREATE TABLE STUDENT_CLASSES (
    student_class_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for student-class relationships
    student_id INT, -- References STUDENT table
    class_id INT, -- References CLASSES table
    class_grade ENUM('A', 'B', 'C', 'D', 'F', 'I') DEFAULT 'I', -- Grade received in the class (A, B, C, D, F, I)
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE, -- Ensures referential integrity on student changes
    FOREIGN KEY (class_id) REFERENCES CLASSES(class_id)
        ON DELETE CASCADE ON UPDATE CASCADE -- Ensures referential integrity on class changes
);
