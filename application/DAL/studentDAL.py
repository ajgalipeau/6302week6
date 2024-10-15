# DAL/studentDAL.py

import mysql.connector
from Connection import MySQLConnection

class StudentDAL:
    """
    Data Access Layer for handling operations related to the 'STUDENT' table in the database.

    Attributes:
    ----------
    connection : MySQLConnection
        An instance of the MySQLConnection class for database operations.

    Methods:
    -------
    add(fname, lname, email, dob, grade):
        Adds a new student record to the database.
    add_using_procedure(fname, lname, email, dob, grade):
        Adds a new student record to the database using a stored procedure.
    read(student_id):
        Reads a student record from the database using the student id.
    read_all():
        Reads all student records from the database.
    read_all_with_classes():
        Reads all student records along with their associated classes and teachers from the database.
    """

    def __init__(self):
        """
        Constructs the necessary attributes for the StudentDAL object.
        """
        self.connection = MySQLConnection(user='admin_user', password='admin1234')
        self.connection.connect()

    def add(self, fname, lname, email, dob, grade):
        """
        Adds a new student record to the database.

        Parameters:
        ----------
        fname : str
            The first name of the student.
        lname : str
            The last name of the student.
        email : str
            The email address of the student.
        dob : str
            The date of birth of the student.
        grade : str
            The grade level of the student.
        """
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
        """
        Adds a new student record to the database using a stored procedure.

        Parameters:
        ----------
        fname : str
            The first name of the student.
        lname : str
            The last name of the student.
        email : str
            The email address of the student.
        dob : str
            The date of birth of the student.
        grade : str
            The grade level of the student.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return

        try:
            query = "CALL InsertStudent(%s, %s, %s, %s, %s)"
            args = (fname, lname, email, dob, grade)
            print(f"Executing: {query} with {args}") # Debugging
            self.connection.execute_query(query, args)
        except mysql.connector.Error as e:
            print(f"Error executing add_using_procedure function: {e}")

    def read(self, student_id):
        """
        Reads a student record from the database using the student id.

        Parameters:
        ----------
        student_id : int
            The unique identifier for the student.

        Returns:
        -------
        dict
            A dictionary containing the student information retrieved from the database.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = "SELECT * FROM STUDENT WHERE student_id = %s"
            result = self.connection.fetch_one(query, (student_id,))
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read query: {e}")
            return None

    def read_all(self):
        """
        Reads all student records from the database.

        Returns:
        -------
        list
            A list of dictionaries, each containing student information retrieved from the database.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = "SELECT * FROM STUDENT"
            result = self.connection.fetch_all(query)
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read_all query: {e}")
            return None
        
    def read_all_with_classes(self):
        """
        Reads all student records along with their associated classes and teachers from the database.

        Returns:
        -------
        list
            A list of dictionaries, each containing student information along with their associated classes and teachers retrieved from the database.
        """
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