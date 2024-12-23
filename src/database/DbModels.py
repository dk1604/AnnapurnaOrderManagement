from sqlalchemy import Column, String, Integer, VARCHAR, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomAlembicVersion(Base):
    __tablename__ = 'canteen_alembic_version'
    version_num = Column(String(32), primary_key=True)


class menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(250))
    description = Column(VARCHAR(250))
    price = Column(Integer)
