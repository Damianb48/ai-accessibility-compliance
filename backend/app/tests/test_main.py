from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_and_get_scan() -> None:
    """Ensure a scan can be created and subsequently retrieved."""
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    scan_id = data["id"]
    # Retrieve the scan immediately; status may still be pending
    response2 = client.get(f"/scan/{scan_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["id"] == scan_id
    assert data2["url"] == "https://example.com/"
