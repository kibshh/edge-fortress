from fastapi import FastAPI
from pydantic import BaseModel

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float
    
app = FastAPI(title="Edge Fortress API", version="0.0.1")

@app.get("/health")
def health():
    # simple liveness probe for monitoring
    return {"status": "ok"}

@app.post("/ingest")
def ingest(r: Reading):
    # echo back
    return {"accepted": True, "echo": r.model_dump()}