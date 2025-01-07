from sqlalchemy import Column, String, Integer, VARCHAR, Numeric, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


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
    payment_mode = Column(String(50), nullable=True)
    user_name = Column(String(250), nullable=True)
    user_phone = Column(String(100), nullable=True)
    order_date = Column(BigInteger, nullable=False)

