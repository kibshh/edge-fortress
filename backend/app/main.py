from fastapi import FastAPI
from pydantic import BaseModel
import os
from datetime import datetime, timezone
from typing import List

# read configuration from environment with safe defaults
APP_NAME = os.getenv("APP_NAME", "Edge Fortress API")
APP_ENV = os.getenv("APP_ENV", "local")
HEALTH_MESSAGE = os.getenv("HEALTH_MESSAGE", "ok")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float
    unit: str | None = None
    timestamp: datetime | None = None
    
app = FastAPI(title=APP_NAME, version="0.0.1")

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
    return {
        "accepted": True,
        "reading": {
            "device_id": r.device_id,
            "metric": r.metric,
            "value": r.value,
            "unit": r.unit,
            "timestamp": r.timestamp.isoformat()
        }
    }

@app.post("/ingest_batch")
def ingest_batch(readings: List[Reading]):
    normalized = []
    for r in readings:
        # if device didn't send a timestamp, use server time
        if r.timestamp is None:
            r.timestamp = datetime.now(timezone.utc)
        normalized.append({
            "device_id": r.device_id,
            "metric": r.metric,
            "value": r.value,
            "unit": r.unit,
            "timestamp": r.timestamp.isoformat()
        })

    return {
        "accepted": True,
        "count": len(normalized),
        "readings": normalized
    }
