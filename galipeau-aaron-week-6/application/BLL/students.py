# BLL/students.py
from DAL.studentDAL import StudentDAL

# Student Class
class Student:
    def __init__(self, id=None, first_name=None, last_name=None, email=None, date_of_birth=None, grade=None):
        self.studentDal = StudentDAL()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.grade = grade

    def add(self):
        self.studentDal.add_using_procedure(
            self.first_name,
            self.last_name,
            self.email,
            self.date_of_birth,
            self.grade
        )
    
    def getStudentsWithClasses(self):
        return self.studentDal.read_all_with_classes()