from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat():
    resp = client.post("/chat", json={"session_id": "test1", "message": "Hello"})
    assert resp.status_code == 200
    assert "reply" in resp.json()
