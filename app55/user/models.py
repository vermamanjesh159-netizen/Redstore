from sqlalchemy import Column, Integer, String
from app5.database import Base

class Payment(Base):
    __tablename__ = 'user_payment'
    
    txnid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(50), nullable=False)
    amt = Column(String(50), nullable=False)
    info = Column(String(50), nullable=False)
