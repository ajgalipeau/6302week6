-- galipeau permissions.sql

-- Create roles for different access levels
CREATE ROLE IF NOT EXISTS 'admin_role';
CREATE ROLE IF NOT EXISTS 'read_role';
CREATE ROLE IF NOT EXISTS 'modify_role';

-- Admin role has full privileges and can grant options to others
GRANT ALL PRIVILEGES ON SCHOOL.* TO 'admin_role' WITH GRANT OPTION;

-- Read role can only SELECT data and EXECUTE read-related procedures/functions
GRANT SELECT ON SCHOOL.* TO 'read_role';

-- Grant execute permissions on read-related functions
GRANT EXECUTE ON FUNCTION SCHOOL.get_student_id TO 'read_role';
GRANT EXECUTE ON FUNCTION SCHOOL.getTeacherId TO 'read_role';

-- Grant execute permissions on read-related procedures
GRANT EXECUTE ON PROCEDURE SCHOOL.getAllStudents TO 'read_role';
GRANT EXECUTE ON PROCEDURE SCHOOL.getStudentsWithClasses TO 'read_role';
GRANT EXECUTE ON PROCEDURE SCHOOL.getTeacherStudents TO 'read_role';
GRANT EXECUTE ON PROCEDURE SCHOOL.getStudentAverageGrades TO 'read_role';
GRANT EXECUTE ON PROCEDURE SCHOOL.getStudentGPA TO 'read_role';

-- Modify role can SELECT, INSERT, UPDATE, DELETE data and EXECUTE modify-related procedures/functions
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHOOL.* TO 'modify_role';

-- Grant execute permissions on modify-related procedures/functions
GRANT EXECUTE ON PROCEDURE SCHOOL.InsertStudent TO 'modify_role';
GRANT EXECUTE ON FUNCTION SCHOOL.addStudent TO 'modify_role';

-- Grant execute permissions on admin-related procedures/functions
GRANT EXECUTE ON PROCEDURE SCHOOL.DeleteAllStudents TO 'admin_role'; -- Existing admin-only procedure
GRANT EXECUTE ON PROCEDURE SCHOOL.UpdateTeacherEmail TO 'admin_role'; -- New admin-only procedure

-- Assigning roles to users
GRANT 'read_role' TO 'read_only'@'%';
GRANT 'modify_role' TO 'modify_user'@'%';
GRANT 'admin_role' TO 'admin_user'@'%';

-- Set default roles for each user
SET DEFAULT ROLE 'admin_role' TO 'admin_user';
SET DEFAULT ROLE 'read_role' TO 'read_only';
SET DEFAULT ROLE 'modify_role' TO 'modify_user';

-- Display grants for verification
SHOW GRANTS FOR 'admin_user';
SHOW GRANTS FOR 'modify_user';
SHOW GRANTS FOR 'read_only';

-- Flush privileges to ensure changes are applied
FLUSH PRIVILEGES;
