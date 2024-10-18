# BLL/students.py

from DAL.studentDAL import StudentDAL
import logging

# Student Class
class Student:
    def __init__(self, role='admin_user', id=None, first_name=None, last_name=None, email=None, date_of_birth=None, grade=None):
        """
        Initialize the Student object with the specified role.
        Roles: 'read_only', 'modify_user', 'admin_user'
        """
        self.studentDal = StudentDAL()
        self.role = role
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.grade = grade
        logging.info(f"Initialized Student object with role: {role}")

    def add(self):
        """
        Adds a new student using the stored procedure.
        """
        if self.role != 'modify_user' and self.role != 'admin_user':
            logging.error("Unauthorized attempt to add a student.")
            raise PermissionError("You do not have permission to add a student.")
        
        self.studentDal.add_using_procedure(
            self.first_name,
            self.last_name,
            self.email,
            self.date_of_birth,
            self.grade
        )
        logging.info(f"Called add_using_procedure for student: {self.first_name} {self.last_name}")
    
    def getStudentsWithClasses(self):
        """
        Retrieves all students along with their classes and grades.
        """
        students = self.studentDal.read_all_with_classes()
        logging.info("Retrieved students with classes.")
        return students
    
    # Additional methods for admin operations
    def deleteAllStudents(self):
        """
        Deletes all students from the STUDENT table.
        This operation is restricted to admin users only.
        """
        if self.role != 'admin_user':
            logging.error("Unauthorized attempt to delete all students.")
            raise PermissionError("You do not have permission to delete all students.")
        
        self.studentDal.deleteAllStudents()
    
    def updateTeacherEmail(self, t_id, new_email):
        """
        Updates a teacher's email address.
        This operation is restricted to admin users only.
        """
        if self.role != 'admin_user':
            logging.error("Unauthorized attempt to update teacher email.")
            raise PermissionError("You do not have permission to update teacher email.")
        
        self.studentDal.updateTeacherEmail(t_id, new_email)
    
    def disconnect(self):
        """
        Disconnects all DAL connections.
        """
        self.studentDal.disconnect()
