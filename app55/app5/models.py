from sqlalchemy import Column, Integer, String
from .database import Base

class Register(Base):
    __tablename__ = 'app5_register'
    
    regid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(15), nullable=False)
    mobile = Column(String(12), nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(20), nullable=False)
    gender = Column(String(10), nullable=False)
    status = Column(Integer, nullable=False)
    roll = Column(String(10), nullable=False)
    info = Column(String(50), nullable=False)

class test1(Base):
    __tablename__ = 'app5_test1'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(15))
    mobile = Column(String(12))
    address = Column(String(500))
    gender = Column(String(10))
