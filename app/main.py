from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from model import SensorReading
from schema import SensorReadingCreate, SensorReadingResponse
from mqtt_client import start_mqtt


# Create database tables if they don't already exist
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start MQTT subscriber
    mqtt_client = start_mqtt()

    print("NEXUS MQTT subscriber started")

    yield

    # Stop MQTT subscriber when FastAPI shuts down
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

    print("NEXUS MQTT subscriber stopped")


app = FastAPI(
    title="NEXUS Backend",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "message": "NEXUS API is running"
    }


@app.post(
    "/readings",
    response_model=SensorReadingResponse,
    status_code=201
)
def create_reading(
    payload: SensorReadingCreate,
    db: Session = Depends(get_db)
):
    reading = SensorReading(
        **payload.model_dump()
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return reading


@app.get(
    "/latest",
    response_model=SensorReadingResponse
)
def latest(
    db: Session = Depends(get_db)
):
    reading = (
        db.query(SensorReading)
        .order_by(SensorReading.time.desc())
        .first()
    )

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="No telemetry found"
        )

    return reading


@app.get(
    "/history",
    response_model=list[SensorReadingResponse]
)
def history(
    db: Session = Depends(get_db)
):
    return (
        db.query(SensorReading)
        .order_by(SensorReading.time.desc())
        .limit(10)
        .all()
    )