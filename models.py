from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(100),unique=True,index=True)
    email=Column(String(100))
    hashed_password=Column(String(512))

class Memo(Base):
    __tablename__='memo'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100),nullable=False)
    content =Column(String(1000),nullable=False)
    user_id=Column(Integer,ForeignKey('users.id'))
    user=relationship("User")

