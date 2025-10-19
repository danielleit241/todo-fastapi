from app.config import settings

def test_create_user(client):
    """Test creating a new user via API."""
    user_data = {
        "email": "test@example.com",
        "password": "SecureP@ssw0rd!"
    }

    response = client.post(f"{settings.API_PREFIX}/users/", json=user_data)

    assert response.status_code == 201