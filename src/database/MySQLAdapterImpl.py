import mysql.connector
from mysql.connector import Error
from src.database import Adaptor


class MySQLAdapterImpl:
    print("\n2............")

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        print("\nMySQL Adapter Initialized")

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print(f"Connected to MySQL database: {self.database}")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            raise

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Disconnected from the MySQL database.")

    def execute_query(self, query, params=None):
        if self.connection is None:
            print("No database connection. Please connect first.")
            return []
        try:
            print("\ninside execute_query......")
            self.cursor.execute(query, params or ())
            self.connection.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching all data: {e}")
            return None

    def fetch_one(self, query, params=None):
        print("\n query..........", query)
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching by id data: {e}")
            return None
