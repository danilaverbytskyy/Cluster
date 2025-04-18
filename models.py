from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_vk_id = Column(Integer, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(Integer, nullable=False)
    is_closed = Column(Boolean, nullable=False)
    date_of_recording = Column(Date, nullable=False)
    bdate = Column(String, nullable=True)
    city = Column(String, nullable=True)
    # country = Column(String, nullable=True)
    # home_town = Column(String, nullable=True)
    # photo_max_orig = Column(String, nullable=True)
    # status = Column(String, nullable=True)
    last_seen = Column(Date, nullable=True)
    followers_count = Column(Integer, nullable=True)
    occupation = Column(String, nullable=True)
    relation = Column(Integer, nullable=True)

    # Define relationship
    groups = relationship("UserGroup", back_populates="user")


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    group_vk_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    members_count = Column(Integer, default=0)
    is_closed = Column(Boolean, nullable=False)

    users = relationship("UserGroup", back_populates="group")


class UserGroup(Base):
    __tablename__ = 'user_groups'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")
