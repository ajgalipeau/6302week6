# BLL/students.py
from DAL.studentDAL import StudentDAL
from DAL.teacherDAL import TeacherDAL
from DAL.classesDAL import ClassesDAL

# Student Class
class Student:
    """
    The Student class represents a student entity and provides methods to interact with the student data.
    Attributes:
        id (int, optional): The unique identifier for the student.
        first_name (str, optional): The first name of the student.
        last_name (str, optional): The last name of the student.
        email (str, optional): The email address of the student.
        date_of_birth (str, optional): The date of birth of the student.
        grade (str, optional): The grade of the student.
    Methods:
        add():
            Adds a new student record using a stored procedure.
        read():
            Reads the student record based on the student's ID.
        getStudents():
            Retrieves all student records.
        getStudentsWithClasses():
            Retrieves all student records along with their associated classes.
    """
    def __init__(self, id=None, first_name=None, last_name=None, email=None, date_of_birth=None, grade=None):
        """
        Initializes a new instance of the Student class.

        Args:
            id (int, optional): The unique identifier for the student. Defaults to None.
            first_name (str, optional): The first name of the student. Defaults to None.
            last_name (str, optional): The last name of the student. Defaults to None.
            email (str, optional): The email address of the student. Defaults to None.
            date_of_birth (str, optional): The date of birth of the student. Defaults to None.
            grade (str, optional): The grade of the student. Defaults to None.
        """
        self.studentDal = StudentDAL()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.grade = grade

    def add(self):
        """
        Adds a new student record to the database using a stored procedure.

        This method calls the `add_using_procedure` method of the `studentDal` object,
        passing the student's first name, last name, email, date of birth, and grade
        as parameters.

        Parameters:
        None

        Returns:
        None
        """
        self.studentDal.add_using_procedure(
            self.first_name,
            self.last_name,
            self.email,
            self.date_of_birth,
            self.grade
        )

    def read(self):
        """
        Reads the student data from the data access layer (DAL) using the student's ID.

        Returns:
            dict: A dictionary containing the student's data.
        """
        return self.studentDal.read(self.id)
    
    def getStudents(self):
        """
        Retrieves a list of all students from the data access layer.

        Returns:
            list: A list of student records.
        """
        return self.studentDal.read_all()
    
    def getStudentsWithClasses(self):
        """
        Retrieves a list of students along with their associated classes.

        Returns:
            list: A list of dictionaries, where each dictionary contains student information
                  and their associated classes.
        """
        return self.studentDal.read_all_with_classes()

class Teacher:
    """
    A class to represent a teacher.

    Attributes:
    ----------
    id : int, optional
        The unique identifier for the teacher (default is None).
    first_name : str, optional
        The first name of the teacher (default is None).
    last_name : str, optional
        The last name of the teacher (default is None).
    email : str, optional
        The email address of the teacher (default is None).
    teacherDal : TeacherDAL
        An instance of the TeacherDAL class for database operations.

    Methods:
    -------
    add():
        Adds the teacher's information to the database.
    read():
        Reads the teacher's information from the database using the teacher's id.
    """

    def __init__(self, id=None, first_name=None, last_name=None, email=None):
        """
        Constructs all the necessary attributes for the teacher object.

        Parameters:
        ----------
        id : int, optional
            The unique identifier for the teacher (default is None).
        first_name : str, optional
            The first name of the teacher (default is None).
        last_name : str, optional
            The last name of the teacher (default is None).
        email : str, optional
            The email address of the teacher (default is None).
        """
        self.teacherDal = TeacherDAL()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def add(self):
        """
        Adds the teacher's information to the database.

        This method uses the TeacherDAL instance to add the teacher's
        first name, last name, and email to the database.
        """
        self.teacherDal.add(
            self.first_name,
            self.last_name,
            self.email
        )

    def read(self):
        """
        Reads the teacher's information from the database using the teacher's id.

        Returns:
        -------
        dict
            A dictionary containing the teacher's information retrieved from the database.
        """
        return self.teacherDal.read(self.id)

class Class:
    """
    A class to represent a school class.

    Attributes:
    ----------
    id : int, optional
        The unique identifier for the class (default is None).
    room_number : str, optional
        The room number where the class is held (default is None).
    subject : str, optional
        The subject taught in the class (default is None).
    class_grade : str, optional
        The grade level of the class (default is None).
    teacher_id : int, optional
        The unique identifier for the teacher of the class (default is None).
    student_id : int, optional
        The unique identifier for the student in the class (default is None).
    classDal : ClassesDAL
        An instance of the ClassesDAL class for database operations.

    Methods:
    -------
    add():
        Adds the class information to the database.
    read():
        Reads the class information from the database using the class id.
    """

    def __init__(self, id=None, room_number=None, subject=None, class_grade=None, teacher_id=None, student_id=None):
        """
        Constructs all the necessary attributes for the class object.

        Parameters:
        ----------
        id : int, optional
            The unique identifier for the class (default is None).
        room_number : str, optional
            The room number where the class is held (default is None).
        subject : str, optional
            The subject taught in the class (default is None).
        class_grade : str, optional
            The grade level of the class (default is None).
        teacher_id : int, optional
            The unique identifier for the teacher of the class (default is None).
        student_id : int, optional
            The unique identifier for the student in the class (default is None).
        """
        self.classDal = ClassesDAL()
        self.id = id
        self.room_number = room_number
        self.subject = subject
        self.class_grade = class_grade
        self.teacher_id = teacher_id
        self.student_id = student_id

    def add(self):
        """
        Adds the class information to the database.

        This method uses the ClassesDAL instance to add the class's
        room number, subject, class grade, teacher id, and student id to the database.
        """
        self.classDal.add(
            self.room_number,
            self.subject,
            self.class_grade,
            self.teacher_id,
            self.student_id
        )

    def read(self):
        """
        Reads the class information from the database using the class id.

        Returns:
        -------
        dict
            A dictionary containing the class information retrieved from the database.
        """
        return self.classDal.read(self.id)
