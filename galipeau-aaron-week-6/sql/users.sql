-- galipeau users.sql

-- Create admin user with full privileges
CREATE USER IF NOT EXISTS 'admin_user'@'%' IDENTIFIED WITH caching_sha2_password BY 'admin1234';

-- Create modify user for inserting, updating, and deleting data
CREATE USER IF NOT EXISTS 'modify_user'@'%' IDENTIFIED WITH caching_sha2_password BY 'modify1234';

-- Create two read-only users with identical privileges
CREATE USER IF NOT EXISTS 'read_only'@'%' IDENTIFIED WITH caching_sha2_password BY 'read1234';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;