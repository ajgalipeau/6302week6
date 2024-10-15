import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self, user, password):
        self.host = "127.0.0.1"
        self.database = "SCHOOL"
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            # Create a connection to the MySQL database
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"Connected to MySQL Server version {db_info}")
                print(f"You're connected to the database: {self.database}")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed.")

    def execute_query(self, query, params=None):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                self.connection.commit()
                print(f"Query executed: {query}")
            except Error as e:
                print(f"Error executing query: {e}")
            finally:
                cursor.close()

    def fetch_all(self, query, params=None):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Error fetching data: {e}")
                return None
            finally:
                cursor.close()

    def fetch_one(self, query, params=None):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
            except Error as e:
                print(f"Error fetching data: {e}")
                return None
            finally:
                cursor.close()