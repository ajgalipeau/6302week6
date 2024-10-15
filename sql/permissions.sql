-- galipeau permissions.sql

CREATE ROLE IF NOT EXISTS 'admin_role';
CREATE ROLE IF NOT EXISTS 'read_role';
CREATE ROLE IF NOT EXISTS 'modify_role';

-- Admin role has full privileges and can grant options to others
GRANT ALL PRIVILEGES ON SCHOOL.* TO 'admin_role' WITH GRANT OPTION;

-- Read role can only SELECT data
GRANT SELECT ON SCHOOL.* TO 'read_role';

-- Modify role can INSERT, UPDATE, and DELETE data
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHOOL.* TO 'modify_role';

-- Assigning roles to users
GRANT 'admin_role' TO 'admin_user'@'%';
GRANT 'read_role' TO 'read_only'@'%';
GRANT 'modify_role' TO 'modify_user'@'%';

-- Set default roles for each user
SET DEFAULT ROLE 'admin_role' TO 'admin_user';
SET DEFAULT ROLE 'read_role' TO 'read_only';
SET DEFAULT ROLE 'modify_role' TO 'modify_user';

-- Display grants for verification
SHOW GRANTS FOR 'admin_user';
SHOW GRANTS FOR 'read_only';
SHOW GRANTS FOR 'modify_user';

-- Flush privileges to ensure changes are applied
FLUSH PRIVILEGES;
