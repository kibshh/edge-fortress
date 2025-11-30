from fastapi.testclient import TestClient
from app.main import app, latest_readings

client = TestClient(app)


def setup_function():
    """
    Pytest will run this before each test function in this file.
    We clear latest_readings so tests don't interfere with each other.
    """
    latest_readings.clear()


def test_readings_returns_multiple_for_device():
    # Arrange: send a batch with temperature and humidity
    payload = [
        {
            "device_id": "esp32-001",
            "metric": "temperature",
            "value": 23.5,
            "unit": "C",
        },
        {
            "device_id": "esp32-001",
            "metric": "humidity",
            "value": 40.0,
            "unit": "%",
        },
    ]

    resp = client.post("/ingest_batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["accepted"] is True
    assert data["count"] == 2

    # Act: call /readings for that device
    resp2 = client.get("/readings", params={"device_id": "esp32-001", "limit": 10})
    assert resp2.status_code == 200
    readings_data = resp2.json()

    # Assert: we got back both readings
    assert readings_data["device_id"] == "esp32-001"
    assert readings_data["count"] == 2
    metrics = [r["metric"] for r in readings_data["readings"]]
    assert "temperature" in metrics
    assert "humidity" in metrics


def test_readings_filters_by_metric():
    # Arrange: send two metrics again
    payload = [
        {
            "device_id": "esp32-001",
            "metric": "temperature",
            "value": 23.5,
            "unit": "C",
        },
        {
            "device_id": "esp32-001",
            "metric": "humidity",
            "value": 40.0,
            "unit": "%",
        },
    ]

    resp = client.post("/ingest_batch", json=payload)
    assert resp.status_code == 200

    # Act: ask only for humidity readings
    resp2 = client.get(
        "/readings",
        params={"device_id": "esp32-001", "metric": "humidity", "limit": 10},
    )
    assert resp2.status_code == 200
    readings_data = resp2.json()

    # Assert: only humidity comes back
    assert readings_data["device_id"] == "esp32-001"
    assert readings_data["count"] == 1
    assert readings_data["readings"][0]["metric"] == "humidity"
    assert readings_data["readings"][0]["value"] == 40.0

def test_latest_returns_all_recent_for_device():
    latest_readings.clear()

    payload = [
        {
            "device_id": "esp32-001",
            "metric": "temperature",
            "value": 23.5,
            "unit": "C",
        },
        {
            "device_id": "esp32-001",
            "metric": "humidity",
            "value": 40.0,
            "unit": "%",
        },
    ]

    resp = client.post("/ingest_batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["accepted"] is True
    assert data["count"] == 2

    # Act: call /latest with overlarge limit
    resp2 = client.get("/latest", params={"device_id": "esp32-001", "limit": 10})
    assert resp2.status_code == 200
    latest_data = resp2.json()

    # Assert
    assert latest_data["device_id"] == "esp32-001"
    assert latest_data["count"] == 2
    assert len(latest_data["readings"]) == 2

    metrics = [r["metric"] for r in latest_data["readings"]]
    assert metrics == ["temperature", "humidity"] 


def test_latest_respects_limit_and_returns_most_recent():
    latest_readings.clear()

    payload = [
        {
            "device_id": "esp32-001",
            "metric": "temperature",
            "value": 23.5,
            "unit": "C",
        },
        {
            "device_id": "esp32-001",
            "metric": "humidity",
            "value": 40.0,
            "unit": "%",
        },
        {
            "device_id": "esp32-001",
            "metric": "temperature",
            "value": 24.0,
            "unit": "C",
        },
    ]

    resp = client.post("/ingest_batch", json=payload)
    assert resp.status_code == 200

    resp2 = client.get("/latest", params={"device_id": "esp32-001", "limit": 1})
    assert resp2.status_code == 200
    latest_data = resp2.json()

    assert latest_data["count"] == 1
    assert len(latest_data["readings"]) == 1

    last = latest_data["readings"][0]
    assert last["metric"] == "temperature"
    assert last["value"] == 24.0

