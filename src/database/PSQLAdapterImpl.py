import logging
import sys

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, String, Integer, VARCHAR, create_engine, Numeric, Date
from sqlalchemy.orm import declarative_base
from Properties import user, password, host, port, database

Base = declarative_base()
metadata = Base.metadata


def handle_exception(exc_type, exc_value, exc_tb):
    if exc_type == KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    else:
        # Custom behavior for uncaught exceptions (e.g., log it without printing the full stack trace)
        print(f"Handled exception: {exc_value}")

sys.excepthook = handle_exception

class CustomAlembicVersion(Base):
    __tablename__ = 'canteen_alembic_version'
    version_num = Column(String(32), primary_key=True)


class menu(Base):
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



class PSQLAdapterImpl:

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.engine = None
        logging.error("PSQL Adapter Initialized")

    _engine = None

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
            engine = PSQLAdapterImpl.get_engine()
            cls._session_factory = scoped_session(sessionmaker(bind=engine))
        return cls._session_factory()
