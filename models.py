from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    icao = Column(String, unique=True, index=True)
    iata = Column(String, index=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(String)
    longitude = Column(String)
