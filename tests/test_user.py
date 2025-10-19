from app.config import settings
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user():
    """Test creating a new user via API."""
    user_data = {
        "email": "test@example.com",
        "password": "SecureP@ssw0rd!"
    }

    response = client.post(f"{settings.API_PREFIX}/users/", json=user_data)

    assert response.status_code == 201