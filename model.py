from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Post(Base):
    __tablename__ = "Posts"
    post_id = Column(Integer, primary_key=True, index=True)
    title_post = Column(String)
    user_id = Column(Integer)
    description = Column(String)
    likes = Column(Integer)
    creation_date = Column(DateTime)


class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_age = Column(Integer)
    career = Column(String)
    rol_id = Column(Integer)
    semester = Column(Integer)
    friends_list = Column(String)


class Rol(Base):
    __tablename__ = "Rol"
    rol_id = Column(Integer, primary_key=True, index=True)
    rol_description = Column(String)
