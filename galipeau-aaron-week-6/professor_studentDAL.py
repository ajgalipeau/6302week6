# professor_studentDAL.py

import mysql.connector

class StudentDAL:
	def __init__(self):
		self.admin_cnx = mysql.connector.connect(user='admin_user',
												 password='admin1234',
												 host='127.0.0.1',
												 database='SCHOOL')
		self.read_cnx = mysql.connector.connect(user='read_only',
												password='read1234',
												host='127.0.0.1',
												database='school')
		self.write_cnx = mysql.connector.connect(user='modify_user',
												 password='modify1234',
												 host='127.0.0.1',
												 database='school')

	def getStudents(self):
		cursor = self.read_cnx.cursor(dictionary=True)
		cursor.callproc('getStudents')
		self.read_cnx.commit()
		list = []
		for result in cursor.stored_results():
			for item in result.fetchall():
				list.append((item['first_name'], item['last_name'], item['email']))
		cursor.close()
		return list

	def addStudent(self, fname, lname, email):
		cursor = self.write_cnx.cursor(dictionary=True)
		query = ("SELECT addStudent(%s, %s, %s)")
		args = (fname, lname, email)
		cursor.execute(query, args)
		result = cursor.fetchone()
		print(result)
		self.write_cnx.commit()
		cursor.close()
		return result

	def addStudentProc(self, fname, lname, email):
		cursor = self.admin_cnx.cursor(dictionary=True)
		args = (fname, lname, email)
		cursor.callproc('addStudentProc', args)
		self.admin_cnx.commit()
		list = []
		for result in cursor.stored_results():
			for item in result.fetchall():
				list.append((item['first_name'], item['last_name'], item['email']))
		cursor.close()
		return list
