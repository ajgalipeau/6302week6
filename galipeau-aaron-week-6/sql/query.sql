-- galipeau query.sql
-- This script includes key queries to list students, teachers, and their classes,
-- reflecting the correct table relationships in SCHOOL schema.

USE SCHOOL;

-- test modify privileges for test_admin
-- GRANT 'modify_role' TO 'test_admin'@'%';
-- SET DEFAULT ROLE 'modify_role' TO 'test_admin';
-- SHOW GRANTS FOR 'test_admin'@'%';
-- FLUSH PRIVILEGES;

-- archived queries
-- -- Initial query check for students
-- SELECT * FROM STUDENT;


-- -- Query 1: List all students and their associated teachers
-- SELECT 
--     S.first_name AS StudentFirstName, 
--     S.last_name AS StudentLastName, 
--     T.first_name AS TeacherFirstName, 
--     T.last_name AS TeacherLastName
-- FROM 
--     STUDENT_CLASSES SC
-- JOIN 
--     STUDENT S ON SC.student_id = S.student_id
-- JOIN 
--     CLASSES C ON SC.class_id = C.class_id
-- JOIN 
--     TEACHER T ON C.teacher_id = T.teacher_id;

-- -- Query 2: Show all classes with their room number, subject, teacher, and student
-- SELECT 
--     C.class_subject AS ClassSubject, 
--     T.first_name AS TeacherFirstName, 
--     T.last_name AS TeacherLastName, 
--     S.first_name AS StudentFirstName, 
--     S.last_name AS StudentLastName, 
--     SC.class_grade AS Grade
-- FROM 
--     STUDENT_CLASSES SC
-- JOIN 
--     STUDENT S ON SC.student_id = S.student_id
-- JOIN 
--     CLASSES C ON SC.class_id = C.class_id
-- JOIN 
--     TEACHER T ON C.teacher_id = T.teacher_id;

-- -- Query 3: Get details of a specific student by email
-- SELECT 
--     * 
-- FROM 
--     STUDENT 
-- WHERE 
--     email_address = 'eric.neptune@bhms.edu';

-- -- Query 4: List all students, their classes, and grades
-- SELECT 
--     S.first_name AS StudentFirstName, 
--     S.last_name AS StudentLastName, 
--     C.class_subject AS ClassName, 
--     SC.class_grade AS Grade
-- FROM 
--     STUDENT S
-- JOIN 
--     STUDENT_CLASSES SC ON S.student_id = SC.student_id
-- JOIN 
--     CLASSES C ON SC.class_id = C.class_id
-- ORDER BY 
--     S.last_name, S.first_name, C.class_subject;

-- -- Query 5: Retrieve all students
-- SELECT 
--     * 
-- FROM 
--     STUDENT;

-- -- Query 6: Retrieve all teachers
-- SELECT 
--     * 
-- FROM 
--     TEACHER;

-- -- Query 7: Retrieve all classes
-- SELECT 
--     * 
-- FROM 
--     CLASSES;

-- -- Query 8: Retrieve all student-class relationships
-- SELECT 
--     * 
-- FROM 
--     STUDENT_CLASSES;

-- -- Query 9: Get student ID using a function (example)
-- -- Ensure this matches your current schema for testing
-- SELECT 
--     get_student_id('Eric', 'Neptune');

-- -- -- Query 10: Get all students and their grades using a stored procedure
-- -- CALL 
-- --     get_students_grades();

-- -- TESTING
-- CALL InsertStudent('John', 'Doe', 'john.doe@example.com', '2000-01-01', 10);