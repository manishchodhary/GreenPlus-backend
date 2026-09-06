from sqlalchemy import Column, Integer, Float, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    temperature_c = Column(Float)
    humidity_percent = Column(Float)

    soil_moisture = Column(Float)
    soil_score = Column(Float)

    sound_activity = Column(Float)
    sound_score = Column(Float)

    latitude = Column(Float)
    longitude = Column(Float)
    gps_source = Column(Text)