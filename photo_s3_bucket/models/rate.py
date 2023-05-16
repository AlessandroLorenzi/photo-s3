from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rate(Base):
    __tablename__ = 'rates'

    path = Column(String, primary_key=True)
    rate = Column(Integer)
