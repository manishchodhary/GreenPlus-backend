from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
 
from database import get_db, engine, Base
import model
from model import Reading, SensorReading
from schema import ReadingResponse, SensorReadingCreate, SensorReadingResponse

Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
 
def latest_reading(db: Session):
    data = db.query(Reading).order_by(Reading.time.desc()).first()
 
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
 
    return data
 
 
def last_10(db: Session):
    return (
        db.query(Reading)
        .order_by(Reading.time.desc())
        .limit(10)
        .all()
    )
 
 
@app.get("/")
def home():
    return {"message": "API is running"}
 
 
@app.get("/latest", response_model=ReadingResponse)
def latest(db: Session = Depends(get_db)):
    return latest_reading(db)
 
 
@app.get("/history", response_model=list[ReadingResponse])
def history(db: Session = Depends(get_db)):
    return last_10(db)
 
 
@app.post("/readings", response_model=SensorReadingResponse, status_code=201)
def create_reading(payload: SensorReadingCreate, db: Session = Depends(get_db)):
    reading = SensorReading(**payload.model_dump())
 
    db.add(reading)
    db.commit()
    db.refresh(reading)
 
    return reading
 
 
@app.get("/soil/latest")
def soil_latest(db: Session = Depends(get_db)):
    data = latest_reading(db)
 
    return {
        "time": data.time,
        "soil_raw": data.soil_raw,
        "soil_stress": data.soil_stress,
    }
 
 
@app.get("/soil/history")
def soil_history(db: Session = Depends(get_db)):
    rows = last_10(db)
 
    return [
        {
            "time": row.time,
            "soil_raw": row.soil_raw,
            "soil_stress": row.soil_stress,
        }
        for row in rows
    ]
 
 
@app.get("/sound/latest")
def sound_latest(db: Session = Depends(get_db)):
    data = latest_reading(db)
 
    return {
        "time": data.time,
        "sound_raw": data.sound_raw,
        "sound_stress": data.sound_stress,
    }
 
 
@app.get("/sound/history")
def sound_history(db: Session = Depends(get_db)):
    rows = last_10(db)
 
    return [
        {
            "time": row.time,
            "sound_raw": row.sound_raw,
            "sound_stress": row.sound_stress,
        }
        for row in rows
    ]
 
 
@app.get("/temp/latest")
def temp_latest(db: Session = Depends(get_db)):
    data = latest_reading(db)
 
    return {
        "time": data.time,
        "temp_raw": data.temp_raw,
        "temp_stress": data.temp_stress,
    }
 
 
@app.get("/temp/history")
def temp_history(db: Session = Depends(get_db)):
    rows = last_10(db)
 
    return [
        {
            "time": row.time,
            "temp_raw": row.temp_raw,
            "temp_stress": row.temp_stress,
        }
        for row in rows
    ]
 
 
@app.get("/humidity/latest")
def humidity_latest(db: Session = Depends(get_db)):
    data = latest_reading(db)
 
    return {
        "time": data.time,
        "humidity_raw": data.humidity_raw,
        "humidity_stress": data.humidity_stress,
    }
 
 
@app.get("/humidity/history")
def humidity_history(db: Session = Depends(get_db)):
    rows = last_10(db)
 
    return [
        {
            "time": row.time,
            "humidity_raw": row.humidity_raw,
            "humidity_stress": row.humidity_stress,
        }
        for row in rows
    ]
 
 
@app.get("/pir/latest")
def pir_latest(db: Session = Depends(get_db)):
    data = latest_reading(db)
 
    return {
        "time": data.time,
        "pir_raw": data.pir_raw,
        "pir_stress": data.pir_stress,
    }
 
 
@app.get("/pir/history")
def pir_history(db: Session = Depends(get_db)):
    rows = last_10(db)
 
    return [
        {
            "time": row.time,
            "pir_raw": row.pir_raw,
            "pir_stress": row.pir_stress,
        }
        for row in rows
    ]