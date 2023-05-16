from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import Column, DateTime, String

Base = declarative_base()


class Photo(Base):
    __tablename__ = "photos"

    path = Column(String, primary_key=True)
    name = Column(String)
    date_taken = Column(DateTime)
