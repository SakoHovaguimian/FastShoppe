from sqlalchemy import String, Float
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Table, Enum
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.expression import true
from sqlalchemy.ext.associationproxy import association_proxy
from .database import Base

class Tag(Base):

    __tablename__ = "tags"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)

class Item(Base):

    __tablename__ = "items"

    #* Status - 'Of Order'
    ## 0 = pending
    ## 1 = transit
    ## 2 = delivered

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    status = Column(Integer, default=0)
    
    tag_id = Column(Integer, ForeignKey('tags.id'))
    user_id = Column(Integer, ForeignKey('users.id')) #* Because tablename is users

    user = relationship("User")
    tag = relationship("Tag")

class User(Base):
    
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
