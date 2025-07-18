from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def api_key():
    response = client.post("/auth/generate-api-key")
    assert response.status_code == 200
    data = response.json()
    assert "api_key" in data
    return data["api_key"]

def test_post_data(api_key):
    response = client.post("/api/data", headers={"X-API-Key": api_key}, json={
        "zone": "ZoneA",
        "telemetry_name": "temperature",
        "value": 25.5,
        "timestamp": "2025-07-16T18:00:00Z"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["zone"] == "ZoneA"
    assert data["telemetry_name"] == "temperature"
    assert data["value"] == 25.5
    assert "id" in data
    assert "timestamp" in data

def test_get_all_data(api_key):
    response = client.get("/api/data?zone=ZoneA&telemetry_name=temperature", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_summary_bucketed(api_key):
    response = client.get("/api/summary/bucketed?zone=ZoneA&telemetry_name=temperature&from_ts=2025-07-16T00:00:00Z&to_ts=2025-07-17T00:00:00Z", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    data = response.json()
    if len(data) > 0:
        first = data[0]
        assert "bucket" in first
        assert "min" in first
        assert "max" in first
        assert "avg" in first
    else:
        print("No bucketed data found — try inserting more data")

def test_api_key_required():
    response = client.get("/api/data?zone=ZoneA")
    assert response.status_code == 422

def test_api_key_invalid():
    response = client.get("/api/data?zone=ZoneA", headers={"X-API-Key": "wrong"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API key"}

def test_summary_bucketed_invalid_time_range(api_key):
    response = client.get(
        "/api/summary/bucketed?zone=ZoneA&telemetry_name=temperature&from_ts=2025-07-17T10:00:00Z&to_ts=2025-07-16T10:00:00Z", headers={"X-API-Key": api_key}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "from_ts must be before to_ts"}

def test_404_on_invalid_route():
    response = client.get("/invalid-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_post_data_missing_field(api_key):
    response = client.post("/api/data", headers={"X-API-Key": api_key}, json={
        "zone": "ZoneA",
        "value": 25.5,
        "timestamp": "2025-07-16T18:00:00Z"
    })
    assert response.status_code == 422