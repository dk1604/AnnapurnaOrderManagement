import psycopg2
import psycopg2.extras


class PSQLAdapterImpl:
    print("\nStart execution of psql connector adaptor............")

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        print("\nPSQL Adapter Initialized")

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.connection.set_session(autocommit=True)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # For dictionary results

            # If connection is successful
            print(f"Connected to PostgreSQL database: {self.database}")
        except psycopg2.Error as err:
            print(f"Error: {err}")
            self.connection = None

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print(f"Connection to {self.database} closed.")

    def execute_query(self, query, params=None):
        if self.connection is None:
            print("No database connection. Please connect first.")
            return []
        try:
            print("\ninside execute_query......")
            self.cursor.execute(query, params or ())
            self.connection.commit()
            print("Query executed successfully.")

            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()  # Rollback on error

        return []

    def fetch_all(self, query, params=None):
        """Fetch all records from a query"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()  # Returns list of dictionaries
        except psycopg2.Error as e:
            print(f"Error fetching all data: {e}")
            return None

    def fetch_one(self, query, params=None):
        """Fetch one record from a query"""
        try:
            print(f"\nExecuting query: {query}")
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()  # Returns a single row (dictionary) or None
        except psycopg2.Error as e:
            print(f"Error fetching one data: {e}")
            return None
