from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

    json_data = response.json()
    assert "message" in json_data
    assert json_data["message"] == "Welcome to the FastAPI application!"
    
    assert "docs_url" in json_data
    assert json_data["docs_url"] == f"{settings.API_PREFIX}/docs"
    
    assert "redoc_url" in json_data
    assert json_data["redoc_url"] == f"{settings.API_PREFIX}/redoc"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

    json_data = response.json()
    assert "status" in json_data
    assert json_data["status"] == "healthy"
