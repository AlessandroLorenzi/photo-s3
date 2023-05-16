from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Exif(Base):
    __tablename__ = "exifs"

    path = Column(String, primary_key=True)
    model = Column(String)
    make = Column(String)
    iso = Column(Integer)
    aperture = Column(Float)
    shutter_speed = Column(Float)
    exposure_bias = Column(Float)
    exposure_program = Column(Integer)
    rotation = Column(Integer)
    date_taken = Column(DateTime)

