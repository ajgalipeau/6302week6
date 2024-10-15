# DAL/classesDAL.py

import mysql.connector
from Connection import MySQLConnection

class ClassesDAL:
    """
    Data Access Layer for handling operations related to the 'CLASSES' table in the database.

    Attributes:
    ----------
    connection : MySQLConnection
        An instance of the MySQLConnection class for database operations.

    Methods:
    -------
    add(room_number, subject, class_grade, teacher_id, student_id):
        Adds a new class record to the database.
    read(class_id):
        Reads a class record from the database using the class id.
    read_all():
        Reads all class records from the database.
    """

    def __init__(self):
        """
        Constructs the necessary attributes for the ClassesDAL object.
        """
        self.connection = MySQLConnection(user='admin_user', password='admin1234')
        self.connection.connect()

    def add(self, room_number, subject, class_grade, teacher_id, student_id):
        """
        Adds a new class record to the database.

        Parameters:
        ----------
        room_number : str
            The room number where the class is held.
        subject : str
            The subject taught in the class.
        class_grade : str
            The grade level of the class.
        teacher_id : int
            The unique identifier for the teacher of the class.
        student_id : int
            The unique identifier for the student in the class.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return

        try:
            query = "INSERT INTO CLASSES (room_number, subject, class_grade, teacher_id, student_id) VALUES (%s, %s, %s, %s, %s)"
            args = (room_number, subject, class_grade, teacher_id, student_id)
            self.connection.execute_query(query, args)
        except mysql.connector.Error as e:
            print(f"Error executing addClass function: {e}")

    def read(self, class_id):
        """
        Reads a class record from the database using the class id.

        Parameters:
        ----------
        class_id : int
            The unique identifier for the class.

        Returns:
        -------
        dict
            A dictionary containing the class information retrieved from the database.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = "SELECT * FROM CLASSES WHERE class_id = %s"
            result = self.connection.fetch_one(query, (class_id,))
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read query: {e}")
            return None

    def read_all(self):
        """
        Reads all class records from the database.

        Returns:
        -------
        list
            A list of dictionaries, each containing class information retrieved from the database.
        """
        if self.connection.connection is None:
            print("Connection to database failed.")
            return None

        try:
            query = "SELECT * FROM CLASSES"
            result = self.connection.fetch_all(query)
            return result
        except mysql.connector.Error as e:
            print(f"Error executing read_all query: {e}")
            return None
