# Connection.py

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import logging

load_dotenv()  # Load environment variables from .env

# Configure logging to include timestamps and log levels
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()          # Also log to console
    ]
)

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
                logging.info(f"Connected to MySQL Server version {db_info}")
                logging.info(f"You're connected to the database: {self.database} as user: {self.user}")
        except Error as e:
            logging.error(f"Error while connecting to MySQL: {e}")
            self.connection = None
            raise  # Re-raise the exception to be handled by DAL

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            logging.info(f"MySQL connection for user {self.user} is closed.")

    def execute_query(self, query, params=None):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                self.connection.commit()
                logging.info(f"Query executed by {self.user}: {query}")
            except Error as e:
                logging.error(f"Error executing query by {self.user}: {e}")
                raise  # Re-raise the exception to be handled by DAL
            finally:
                cursor.close()

    def fetch_all(self, query, params=None):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                result = cursor.fetchall()
                logging.info(f"Data fetched by {self.user}: {query}")
                return result
            except Error as e:
                logging.error(f"Error fetching data by {self.user}: {e}")
                raise  # Re-raise the exception to be handled by DAL
            finally:
                cursor.close()

    def fetch_one(self, query, params=None):
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()
                logging.info(f"Single record fetched by {self.user}: {query}")
                return result
            except Error as e:
                logging.error(f"Error fetching single record by {self.user}: {e}")
                raise  # Re-raise the exception to be handled by DAL
            finally:
                cursor.close()
