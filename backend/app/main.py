from fastapi import FastAPI
from pydantic import BaseModel
import os

# read configuration from environment with safe defaults
APP_NAME = os.getenv("APP_NAME", "Edge Fortress API")
APP_ENV = os.getenv("APP_ENV", "local")
HEALTH_MESSAGE = os.getenv("HEALTH_MESSAGE", "ok")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float
    
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
    # echo back
    return {"accepted": True, "echo": r.model_dump()}