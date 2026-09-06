from sqlalchemy import Column, Integer, Float, Text, TIMESTAMP
from sqlalchemy.sql import func
 
from database import Base
 
 
class Reading(Base):
    __tablename__ = "readings"
 
    id = Column(Integer, primary_key=True, index=True)
 
    time = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
 
    soil_raw = Column(Float)
    sound_raw = Column(Float)
    temp_raw = Column(Float)
    humidity_raw = Column(Float)
    pir_raw = Column(Integer)
 
    soil_stress = Column(Float)
    sound_stress = Column(Float)
    temp_stress = Column(Float)
    humidity_stress = Column(Float)
    pir_stress = Column(Float)
 
    ems = Column(Float)
 
    alert = Column(Text)
    recommended_action = Column(Text)
 
 
class SensorReading(Base):
    __tablename__ = "sensor_readings"
 
    id = Column(Integer, primary_key=True, index=True)
 
    time = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
 
    temperature_c = Column(Float)
    humidity_percent = Column(Float)
 
    soil_moisture = Column(Float)
    soil_score = Column(Float)
 
    sound_activity = Column(Float)
    sound_score = Column(Float)
 
    latitude = Column(Float)
    longitude = Column(Float)
    gps_source = Column(Text)