from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(Integer, nullable=False)
    is_closed = Column(Boolean, nullable=False)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, unique=True, nullable=False)
