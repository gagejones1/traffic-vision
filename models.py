from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer)
    type = Column(String)
    direction = Column(String)
    crossing_time = Column(Float)
    travel_time = Column(Float)
    speed_mph = Column(Float)