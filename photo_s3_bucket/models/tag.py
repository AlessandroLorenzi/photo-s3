from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'

    path = Column(String, primary_key=True)
    tag = Column(String, primary_key=True)
