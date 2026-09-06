
import asyncio
from contextlib import asynccontextmanager
 
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
 
from database import get_db, engine, Base
from model import SensorReading
from schema import SensorReadingCreate, SensorReadingResponse
from mqtt_client import start_mqtt
import mqtt_client
from connection_manager import manager
 
 
# Create database tables if they don't already exist
Base.metadata.create_all(bind=engine)
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Hand the running event loop to the MQTT thread so it can
    # schedule WebSocket broadcasts from on_message
    mqtt_client.set_main_loop(asyncio.get_event_loop())
 
    # Start MQTT subscriber
    mqtt_client_instance = start_mqtt()
 
    print("NEXUS MQTT subscriber started")
 
    yield
 
    # Stop MQTT subscriber when FastAPI shuts down
    mqtt_client_instance.loop_stop()
    mqtt_client_instance.disconnect()
 
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
 
 
@app.get(
    "/readings/all",
    response_model=list[SensorReadingResponse]
)
def get_all_readings(
    db: Session = Depends(get_db)
):
    return (
        db.query(SensorReading)
        .order_by(SensorReading.time.desc())
        .all()
    )
 
 
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()   # keeps connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)