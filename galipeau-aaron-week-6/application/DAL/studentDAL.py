# DAL/studentDAL.py

import os
from Connection import MySQLConnection
import logging
import mysql.connector

class StudentDAL:
    def __init__(self):
        """
        Initialize the DAL with connections for different roles.
        """
        # Initialize connections for each role
        self.read_connection = MySQLConnection(user=os.getenv('READ_USER'),
                                               password=os.getenv('READ_PASSWORD'))
        self.modify_connection = MySQLConnection(user=os.getenv('MODIFY_USER'),
                                                 password=os.getenv('MODIFY_PASSWORD'))
        # Connect both connections
        self.read_connection.connect()
        self.modify_connection.connect()
        logging.info("Initialized StudentDAL with read and modify connections.")

    def addStudent(self, fname, lname, email, dob, grade):
        """
        Adds a new student directly via SQL INSERT using modify_role.
        """
        try:
            query = """
                INSERT INTO STUDENT (first_name, last_name, email_address, date_of_birth, student_grade)
                VALUES (%s, %s, %s, %s, %s)
            """
            args = (fname, lname, email, dob, grade)
            self.modify_connection.execute_query(query, args)
            logging.info(f"Added student: {fname} {lname}")
        except mysql.connector.IntegrityError as e:
            logging.error(f"Integrity error adding student: {e}")
            raise
        except mysql.connector.ProgrammingError as e:
            logging.error(f"Programming error adding student: {e}")
            raise
        except mysql.connector.Error as e:
            logging.error(f"Database error adding student: {e}")
            raise

    def add_using_procedure(self, fname, lname, email, dob, grade):
        """
        Adds a new student using the stored procedure InsertStudent via modify_role.
        """
        try:
            query = "CALL InsertStudent(%s, %s, %s, %s, %s)"
            args = (fname, lname, email, dob, grade)
            self.modify_connection.execute_query(query, args)
            logging.info(f"Executed InsertStudent procedure for: {fname} {lname}")
        except mysql.connector.IntegrityError as e:
            logging.error(f"Integrity error executing InsertStudent: {e}")
            raise
        except mysql.connector.ProgrammingError as e:
            logging.error(f"Programming error executing InsertStudent: {e}")
            raise
        except mysql.connector.Error as e:
            logging.error(f"Database error executing InsertStudent: {e}")
            raise

    def read_all_with_classes(self):
        """
        Retrieves all students along with their classes and grades using read_role.
        """
        try:
            query = """
            SELECT
                S.first_name AS StudentFirstName,
                S.last_name AS StudentLastName,
                S.email_address AS StudentEmail,
                IFNULL(GROUP_CONCAT(C.class_subject ORDER BY C.class_subject SEPARATOR ', '), 'N/A') AS ClassSubjects,
                IFNULL(GROUP_CONCAT(SC.class_grade ORDER BY C.class_subject SEPARATOR ', '), 'N/A') AS ClassGrades,
                IFNULL(GROUP_CONCAT(CONCAT(T.first_name, ' ', T.last_name) ORDER BY C.class_subject SEPARATOR ', '), 'N/A') AS TeacherNames,
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
            LEFT JOIN
                STUDENT_CLASSES SC ON S.student_id = SC.student_id
            LEFT JOIN
                CLASSES C ON SC.class_id = C.class_id
            LEFT JOIN
                TEACHER T ON C.teacher_id = T.teacher_id
            GROUP BY
                S.student_id
            ORDER BY
                S.last_name ASC;
            """
            result = self.read_connection.fetch_all(query)
            logging.info("Fetched all students with classes.")
            return result
        except mysql.connector.Error as e:
            logging.error(f"Error executing read_all_with_classes query: {e}")
            raise

    def deleteAllStudents(self):
        """
        Deletes all students from the STUDENT table using admin_role.
        This operation is restricted to admin users only.
        """
        try:
            # Ensure that only admin_role can perform this operation
            admin_connection = MySQLConnection(user=os.getenv('ADMIN_USER'),
                                               password=os.getenv('ADMIN_PASSWORD'))
            admin_connection.connect()
            query = "CALL DeleteAllStudents()"
            admin_connection.execute_query(query)
            logging.info("All students have been deleted successfully.")
            admin_connection.disconnect()
        except mysql.connector.Error as e:
            logging.error(f"Error executing DeleteAllStudents procedure: {e}")
            raise

    def updateTeacherEmail(self, t_id, new_email):
        """
        Updates a teacher's email address using admin_role.
        This operation is restricted to admin users only.
        """
        try:
            # Ensure that only admin_role can perform this operation
            admin_connection = MySQLConnection(user=os.getenv('ADMIN_USER'),
                                               password=os.getenv('ADMIN_PASSWORD'))
            admin_connection.connect()
            query = "CALL UpdateTeacherEmail(%s, %s)"
            args = (t_id, new_email)
            admin_connection.execute_query(query, args)
            logging.info(f"Teacher ID {t_id} email updated to {new_email}.")
            admin_connection.disconnect()
        except mysql.connector.Error as e:
            logging.error(f"Error executing UpdateTeacherEmail procedure: {e}")
            raise

    def disconnect(self):
        """
        Disconnects all database connections.
        """
        self.read_connection.disconnect()
        self.modify_connection.disconnect()
        logging.info("Disconnected all StudentDAL connections.")
