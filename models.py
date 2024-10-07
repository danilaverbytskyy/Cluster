from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(Integer, nullable=False)
    is_closed = Column(Boolean, nullable=False)
    # bdate = Column(Date, nullable=True)

    groups = relationship("UserGroup", back_populates="user")


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    members_count = Column(Integer, default=0)
    is_closed = Column(Boolean, nullable=False)

    users = relationship("UserGroup", back_populates="group")


class UserGroup(Base):
    __tablename__ = 'user_groups'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")
