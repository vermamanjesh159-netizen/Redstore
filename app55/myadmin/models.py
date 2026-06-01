from sqlalchemy import Column, Integer, String, Float
from app5.database import Base

class products(Base):
    __tablename__ = 'myadmin_products'
    
    prodid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    subcatname = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    ldate = Column(String(10), nullable=False)
    edate = Column(String(10), nullable=False)
    info = Column(String(50), nullable=False)
    prodimage = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
