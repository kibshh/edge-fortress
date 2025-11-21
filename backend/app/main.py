from fastapi import FastAPI
from pydantic import BaseModel
import os
from datetime import datetime, timezone
from typing import List, Dict, Deque
from collections import deque

# read configuration from environment with safe defaults
APP_NAME = os.getenv("APP_NAME", "Edge Fortress API")
APP_ENV = os.getenv("APP_ENV", "local")
HEALTH_MESSAGE = os.getenv("HEALTH_MESSAGE", "ok")
APP_PORT = int(os.getenv("APP_PORT", "8000"))   
MAX_READINGS_PER_DEVICE = 100

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float
    unit: str | None = None
    timestamp: datetime | None = None
    
app = FastAPI(title=APP_NAME, version="0.0.1")

# device_id -> deque of reading dicts (newest at the end)
latest_readings: Dict[str, Deque[dict]] = {}

def store_reading(reading: dict) -> None:
    """
    Store a normalized reading in memory, keeping only the latest
    MAX_READINGS_PER_DEVICE per device_id.
    """
    device_id = reading["device_id"]    
    if device_id not in latest_readings:
        latest_readings[device_id] = deque(maxlen=MAX_READINGS_PER_DEVICE)
    latest_readings[device_id].append(reading)

@app.get("/health")
def health():
    # simple liveness probe for monitoring
    return {
        "status": HEALTH_MESSAGE,
        "env": APP_ENV,
        "name": APP_NAME,
        "port": APP_PORT
        }

@app.post("/ingest")
def ingest(r: Reading):
    # if device didn't send a timestamp, use server time in UTC
    if r.timestamp is None:
        r.timestamp = datetime.now(timezone.utc)
    reading_dict = {
        "device_id": r.device_id,
        "metric": r.metric,
        "value": r.value,
        "unit": r.unit,
        "timestamp": r.timestamp.isoformat()    
    }
    store_reading(reading_dict)
    return {
        "accepted": True,
        "reading": reading_dict
    }

@app.post("/ingest_batch")
def ingest_batch(readings: List[Reading]):
    normalized = []
    for r in readings:
        # if device didn't send a timestamp, use server time
        if r.timestamp is None:
            r.timestamp = datetime.now(timezone.utc)
        reading_dict = {
            "device_id": r.device_id,
            "metric": r.metric,
            "value": r.value,
            "unit": r.unit,
            "timestamp": r.timestamp.isoformat()
        }
        store_reading(reading_dict)
        normalized.append(reading_dict)
    return {
        "accepted": True,
        "count": len(normalized),
        "readings": normalized
    }

@app.get("/latest")
def latest(device_id: str, limit: int = 10):
    """
    Return up to 'limit' latest readings for the given device_id.
    """ 
    # get deque for the device (or an empty list if none)
    readings_for_device = list(latest_readings.get(device_id, []))
    if limit < 0: 
        limit = 0
    latest_slice = readings_for_device[-limit:] if limit > 0 else []
    return {
        "device_id": device_id,
        "count": len(latest_slice),
        "readings": latest_slice
    }
