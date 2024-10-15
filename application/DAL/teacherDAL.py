# DAL/teacherDAL.py

import mysql.connector
from Connection import MySQLConnection

class TeacherDAL:
    """
    Data Access Layer for handling operations related to the 'TEACHER' table in the database.

    Attributes:
    ----------
    connection : MySQLConnection
        An instance of the MySQLConnection class for database operations.

    Methods:
    -------
    add(fname, lname, email):
        Adds a new teacher record to the database.
    read(teacher_id):
        Reads a teacher record from the database using the teacher id.
    read_all():
        Reads all teacher records from the database.
    """

    def __init__(self):
        """
        Constructs the necessary attributes for the TeacherDAL object.
        """
        self.connection = MySQLConnection(user='admin_user', password='admin1234')
        self.connection.connect()

    def add(self, fname, lname, email):
        """
        Adds a new teacher record to the database.

        Parameters:
        ----------
        fname : str
            The first name of the teacher.
        lname : str
            The last name of the teacher.
        email : str
            The email address of the teacher.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return

        try:
            query = "INSERT INTO TEACHER (first_name, last_name, email_address) VALUES (%s, %s, %s)"
            args = (fname, lname, email)
            self.connection.execute_query(query, args)
        except mysql.connector.Error as e:
            print(f"Error executing addTeacher function: {e}")

    def read(self, teacher_id):
        """
        Reads a teacher record from the database using the teacher id.

        Parameters:
        ----------
        teacher_id : int
            The unique identifier for the teacher.

        Returns:
        -------
        dict
            A dictionary containing the teacher information retrieved from the database.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = "SELECT * FROM TEACHER WHERE teacher_id = %s"
            result = self.connection.fetch_one(query, (teacher_id,))
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read query: {e}")
            return None

    def read_all(self):
        """
        Reads all teacher records from the database.

        Returns:
        -------
        list
            A list of dictionaries, each containing teacher information retrieved from the database.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = "SELECT * FROM TEACHER"
            result = self.connection.fetch_all(query)
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read_all query: {e}")
            return None