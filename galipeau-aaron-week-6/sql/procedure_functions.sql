USE SCHOOL;

-- Function to get student ID based on first and last name
DROP FUNCTION IF EXISTS get_student_id;

DELIMITER $$
CREATE FUNCTION get_student_id(firstName VARCHAR(50), lastName VARCHAR(50))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE studentId INT;

    -- Select the student ID based on valid input
    SELECT student_id INTO studentId
    FROM STUDENT
    WHERE first_name = firstName AND last_name = lastName
    LIMIT 1;

    RETURN studentId;
END $$
DELIMITER ;

-- Function to add a new student and return a success message
DROP FUNCTION IF EXISTS addStudent;

DELIMITER $$
CREATE FUNCTION addStudent(
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    email VARCHAR(100),
    dob DATE,
    grade INT
) RETURNS VARCHAR(255)
DETERMINISTIC
MODIFIES SQL DATA
BEGIN
    -- Insert the student data into the table
    INSERT INTO STUDENT (first_name, last_name, email_address, date_of_birth, student_grade)
    VALUES (f_name, l_name, email, dob, grade);
    
    RETURN CONCAT('Student ', f_name, ' ', l_name, ' added successfully.');
END $$
DELIMITER ;

-- Procedure to add a new student using parameters (alternative to the function for insertion)
DROP PROCEDURE IF EXISTS InsertStudent;

DELIMITER $$
CREATE PROCEDURE InsertStudent(
    IN f_name VARCHAR(50),
    IN l_name VARCHAR(50),
    IN email VARCHAR(100),
    IN dob DATE,
    IN grade INT
)
BEGIN
    -- Insert the student data into the table
    INSERT INTO STUDENT (first_name, last_name, email_address, date_of_birth, student_grade)
    VALUES (f_name, l_name, email, dob, grade);
END $$
DELIMITER ;

-- Procedure to get all students
DROP PROCEDURE IF EXISTS getAllStudents;

DELIMITER $$
CREATE PROCEDURE getAllStudents()
BEGIN
    SELECT * FROM STUDENT;
END $$
DELIMITER ;

-- Procedure to get students along with their classes and grades
DROP PROCEDURE IF EXISTS getStudentsWithClasses;

DELIMITER $$
CREATE PROCEDURE getStudentsWithClasses()
BEGIN
    SELECT
        S.first_name AS StudentFirstName,
        S.last_name AS StudentLastName,
        S.email_address AS StudentEmail,
        GROUP_CONCAT(C.class_subject ORDER BY C.class_subject SEPARATOR ', ') AS ClassSubjects,
        GROUP_CONCAT(SC.class_grade ORDER BY C.class_subject SEPARATOR ', ') AS ClassGrades,
        GROUP_CONCAT(CONCAT(T.first_name, ' ', T.last_name) ORDER BY C.class_subject SEPARATOR ', ') AS TeacherNames,
        ROUND(AVG(
            CASE SC.class_grade
                WHEN 'A' THEN 4.0
                WHEN 'B' THEN 3.0
                WHEN 'C' THEN 2.0
                WHEN 'D' THEN 1.0
                WHEN 'F' THEN 0.0
                ELSE 0.0
            END), 2) AS AverageGrade
    FROM
        STUDENT S
    JOIN
        STUDENT_CLASSES SC ON S.student_id = SC.student_id
    JOIN
        CLASSES C ON SC.class_id = C.class_id
    JOIN
        TEACHER T ON C.teacher_id = T.teacher_id
    GROUP BY
        S.student_id
    ORDER BY
        S.last_name ASC;
END $$
DELIMITER ;

-- Procedure to get students taught by a specific teacher
DROP PROCEDURE IF EXISTS getTeacherStudents;

DELIMITER $$
CREATE PROCEDURE getTeacherStudents(
    IN f_name VARCHAR(50),
    IN l_name VARCHAR(50)
)
BEGIN
    DECLARE t_id INT;

    -- Use the getTeacherId function to find the teacher's ID
    SET t_id = getTeacherId(f_name, l_name);

    -- Retrieve students associated with the teacher
    SELECT
        S.first_name AS StudentFirstName,
        S.last_name AS StudentLastName,
        S.email_address AS StudentEmail
    FROM
        CLASSES C
    JOIN
        STUDENT S ON C.student_id = S.student_id
    WHERE
        C.teacher_id = t_id;
END $$
DELIMITER ;

-- Ensure the function getTeacherId exists
DROP FUNCTION IF EXISTS getTeacherId;

DELIMITER $$
CREATE FUNCTION getTeacherId(firstName VARCHAR(50), lastName VARCHAR(50))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE teacherId INT;

    -- Select the teacher ID based on valid input
    SELECT teacher_id INTO teacherId
    FROM TEACHER
    WHERE first_name = firstName AND last_name = lastName
    LIMIT 1;

    RETURN teacherId;
END $$
DELIMITER ;

-- Drop procedure if it exists
DROP PROCEDURE IF EXISTS getStudentAverageGrades;

-- Procedure for Calculating Average Student Grades
DELIMITER $$
CREATE PROCEDURE getStudentAverageGrades()
BEGIN
    SELECT 
        S.student_id AS StudentID,
        S.first_name AS FirstName,
        S.last_name AS LastName,
        ROUND(AVG(
            CASE SC.class_grade
                WHEN 'A' THEN 4.0
                WHEN 'B' THEN 3.0
                WHEN 'C' THEN 2.0
                WHEN 'D' THEN 1.0
                WHEN 'F' THEN 0.0
                ELSE NULL -- Handles any other case for incomplete grades
            END
        ), 2) AS AverageGrade -- Rounds to 2 decimal places
    FROM 
        STUDENT S
    JOIN 
        STUDENT_CLASSES SC ON S.student_id = SC.student_id
    GROUP BY 
        S.student_id;
END $$

DELIMITER ;

-- Drop procedure if it exists
DROP PROCEDURE IF EXISTS getStudentGPA;

-- Procedure for Calculating Average Student Grades (GPA)
DELIMITER $$
CREATE PROCEDURE getStudentGPA()
BEGIN
    SELECT 
        S.student_id AS StudentID,
        S.first_name AS FirstName,
        S.last_name AS LastName,
        ROUND(AVG(
            CASE SC.class_grade
                WHEN 'A' THEN 4.0
                WHEN 'B' THEN 3.0
                WHEN 'C' THEN 2.0
                WHEN 'D' THEN 1.0
                WHEN 'F' THEN 0.0
                WHEN 'I' THEN 0.0
                ELSE 0.0 -- default case for any other input
            END
        ), 2) AS GPA -- Average the decimal values and round to 2 decimal places
    FROM 
        STUDENT S
    JOIN 
        STUDENT_CLASSES SC ON S.student_id = SC.student_id
    GROUP BY 
        S.student_id;
END $$
DELIMITER ;

-- Procedure to delete all students - Admin Only
DROP PROCEDURE IF EXISTS DeleteAllStudents;

DELIMITER $$
CREATE PROCEDURE DeleteAllStudents()
BEGIN
    DELETE FROM STUDENT;
END $$
DELIMITER ;

-- Procedure to update a teacher's email - Admin Only
DROP PROCEDURE IF EXISTS UpdateTeacherEmail;

DELIMITER $$
CREATE PROCEDURE UpdateTeacherEmail(
    IN t_id INT,
    IN new_email VARCHAR(100)
)
BEGIN
    UPDATE TEACHER
    SET email_address = new_email
    WHERE teacher_id = t_id;
END $$
DELIMITER ;

-- Ensure the function getTeacherId exists (already defined above)
DROP FUNCTION IF EXISTS getTeacherId;

DELIMITER $$
CREATE FUNCTION getTeacherId(firstName VARCHAR(50), lastName VARCHAR(50))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE teacherId INT;

    -- Select the teacher ID based on valid input
    SELECT teacher_id INTO teacherId
    FROM TEACHER
    WHERE first_name = firstName AND last_name = lastName
    LIMIT 1;

    RETURN teacherId;
END $$
DELIMITER ;
