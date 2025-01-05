import logging

import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, Column, String, Integer, VARCHAR, Numeric, Date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

import Properties
from src.database import Adaptor

Base = declarative_base()
metadata = Base.metadata


class CustomAlembicVersion(Base):
    __tablename__ = 'canteen_alembic_version'
    version_num = Column(String(32), primary_key=True)


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(250), unique=True, nullable=False)
    description = Column(VARCHAR(250))
    price = Column(Integer)
    food_category = Column(VARCHAR(100))


class CustomerOrder(Base):
    __tablename__ = "customer_order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(100), unique=True, nullable=False)
    order_details = Column(String(500), nullable=False)
    cart_price = Column(Numeric(precision=10, scale=2), nullable=False)
    user_name = Column(String(250), nullable=True)
    user_phone = Column(String(100), nullable=True)
    order_date = Column(Date, nullable=False)



class MySQLAdapterImpl:
    print("\n2............")
    db_url = f"mysql+pymysql://{Properties.user}:{Properties.password}@{Properties.host}:{Properties.port}/{Properties.database}"

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        # self.connection = None
        # self.cursor = None
        self.engine = None
        self.Session = None
        self.session = None
        print("\nMySQL Adapter Initialized")

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                cls.db_url,
                pool_size=10,
                max_overflow=20,
                pool_timeout=120,  # Pool timeout 2 minute
                pool_recycle=3600,  # Recycle connections every hour
                pool_pre_ping=True
            )
        return cls._engine


class SessionFactory:
    _session_factory = None

    @classmethod
    def get_session(cls):
        if cls._session_factory is None:
            engine = MySQLAdapterImpl.get_engine()
            cls._session_factory = scoped_session(sessionmaker(bind=engine))
        return cls._session_factory()

    # def connect(self):
    #     try:
    #         # self.connection = mysql.connector.connect(
    #         #     host=self.host,
    #         #     port=self.port,
    #         #     user=self.user,
    #         #     password=self.password,
    #         #     database=self.database
    #         # )
    #         # if self.connection.is_connected():
    #         #     self.cursor = self.connection.cursor(dictionary=True)
    #         #     print(f"Connected to MySQL database: {self.database}")
    #         """Create a connection to the MySQL database using SQLAlchemy."""
    #         db_url = f"mysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    #         self.engine = create_engine(db_url)
    #         self.Session = sessionmaker(bind=self.engine)
    #         self.session = self.Session()
    #         logging.error("Connected to MySQL database.")
    #     except Error as e:
    #         logging.error(f"Error while connecting to MySQL: {e}")
    #         raise

    def disconnect(self):
        # if self.connection.is_connected():
        #     self.cursor.close()
        #     self.connection.close()
        #     print("Disconnected from the MySQL database.")
        if self.session:
            self.session.close()
            logging.error("Disconnected from the MySQL database.")
        else:
            logging.error("No active session to disconnect.")

    # def execute_query(self, query, params=None):
    #     if self.connection is None:
    #         print("No database connection. Please connect first.")
    #         return []
    #     try:
    #         print("\ninside execute_query......")
    #         self.cursor.execute(query, params or ())
    #         self.connection.commit()
    #         print("Query executed successfully.")
    #     except Error as e:
    #         print(f"Error executing query: {e}")
    #         self.connection.rollback()

    #def fetch_all(self, query, params=None):
    def fetch_all(self, model_class):
        # try:
        #     self.cursor.execute(query, params)
        #     return self.cursor.fetchall()
        # except Error as e:
        #     print(f"Error fetching all data: {e}")
        #     return None
        if not self.session:
            logging.error("No active session. Please connect first.")
            return None

        try:
            results = self.session.query(model_class).all()
            logging.info("Fetched all records.")
            return results
        except SQLAlchemyError as e:
            logging.error(f"Error fetching all data: {e}")
            return None

    # def fetch_one(self, query, params=None):
    #     print("\n query..........", query)
    #     try:
    #         self.cursor.execute(query, params or ())
    #         return self.cursor.fetchone()
    #     except Error as e:
    #         print(f"Error fetching by id data: {e}")
    #         return None
    def fetch_one(self, model_class, **params):
        """Fetch a single record based on the filter criteria."""
        if not self.session:
            logging.error("No active session. Please connect first.")
            return None

        try:
            result = self.session.query(model_class).filter_by(**params).first()
            logging.info("Fetched one record.")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Error fetching data: {e}")
            return None
