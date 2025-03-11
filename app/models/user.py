from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(Integer)
    address = Column(String(100))
    name_contac_emerg = Column(String(100))
    phone_contac_emerg = Column(Integer)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
