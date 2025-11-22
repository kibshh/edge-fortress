from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_defaults():
    """
    When no special environment variables are set,
    /health should return the default config.
    """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    # These are the defaults in main.py when no env vars are provided
    assert data["status"] == "ok"
    assert data["env"] == "local"
    assert data["name"] == "Edge Fortress API"
    assert data["port"] == 8000
