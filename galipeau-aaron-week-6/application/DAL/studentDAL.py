# DAL/studentDAL.py

import mysql.connector
from Connection import MySQLConnection

class StudentDAL:
    def __init__(self):
        self.connection = MySQLConnection(user='admin_user', password='admin1234')
        self.connection.connect()

    def add(self, fname, lname, email, dob, grade):
        if self.connection.connection is None:
            print("Connection to database failed.")
            return

        try:
            query = "INSERT INTO STUDENT (first_name, last_name, email_address, date_of_birth, student_grade) VALUES (%s, %s, %s, %s, %s)"
            args = (fname, lname, email, dob, grade)
            self.connection.execute_query(query, args)
        except mysql.connector.Error as e:
            print(f"Error executing addStudent function: {e}")
            
    def add_using_procedure(self, fname, lname, email, dob, grade):
        if self.connection.connection is None:
            print("Connection to database failed.")
            return

        try:
            query = "CALL InsertStudent(%s, %s, %s, %s, %s)"
            args = (fname, lname, email, dob, grade)
            # print(f"Executing: {query} with {args}") # Debugging
            self.connection.execute_query(query, args)
        except mysql.connector.Error as e:
            print(f"Error executing add_using_procedure function: {e}")
        
    def read_all_with_classes(self):
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = """
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
            result = self.connection.fetch_all(query)
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read_all_with_classes query: {e}")
            return None