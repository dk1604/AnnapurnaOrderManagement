from datetime import datetime

from sqlalchemy import Column, String, Integer, VARCHAR, Numeric, BigInteger, DateTime, Float
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


class VendorExpense(Base):
    __tablename__ = 'vendor_expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor = Column(String(100), nullable=False)
    material = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    payment_mode = Column(String(20), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<VendorExpense(vendor='{self.vendor}', material='{self.material}', amount={self.amount}, payment_mode='{self.payment_mode}', date='{self.date}')>"


