import asyncio
import json
import os
 
import paho.mqtt.client as mqtt
 
from database import SessionLocal
from model import SensorReading
from connection_manager import manager
 
 
MQTT_BROKER = os.getenv("MQTT_BROKER", "10.36.232.114")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "nexus/telemetry")
 
main_loop = None
 
 
def set_main_loop(loop):
    global main_loop
    main_loop = loop
 
 
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"MQTT connection failed: {reason_code}")
 
 
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
 
        print("MQTT telemetry received:")
        print(data)
 
        reading = SensorReading(**data)
 
        db = SessionLocal()
 
        try:
            db.add(reading)
            db.commit()
            db.refresh(reading)
 
            print(f"Saved telemetry with ID: {reading.id}")
 
            if main_loop:
                asyncio.run_coroutine_threadsafe(
                    manager.broadcast({
                        "id": reading.id,
                        "time": reading.time.isoformat(),
                        "temperature_c": reading.temperature_c,
                        "humidity_percent": reading.humidity_percent,
                        "soil_moisture": reading.soil_moisture,
                        "soil_score": reading.soil_score,
                        "sound_activity": reading.sound_activity,
                        "sound_score": reading.sound_score,
                        "latitude": reading.latitude,
                        "longitude": reading.longitude,
                        "gps_source": reading.gps_source,
                    }),
                    main_loop
                )
 
        finally:
            db.close()
 
    except json.JSONDecodeError:
        print("Invalid JSON received from MQTT")
 
    except Exception as e:
        print(f"MQTT processing error: {e}")
 
 
def start_mqtt():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )
 
    client.on_connect = on_connect
    client.on_message = on_message
 
    client.connect(
        MQTT_BROKER,
        MQTT_PORT
    )
 
    client.loop_start()
 
    return client
 