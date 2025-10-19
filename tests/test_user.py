import pytest
from app.schemas import user
from app.config import settings

@pytest.mark.parametrize("email, password", [
    ("test@example.com", "SecureP@ssw0rd!"),
    ("user@example.com", "AnotherP@ssw0rd!"),
    ("admin@example.com", "AdminP@ssw0rd!")
])
def test_get_all_users_success_with_response_200(client, create_token, email, password):
    """Test retrieving all users via API."""
    token = create_token(email=email, password=password)
    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }
    response = client.get(f"{settings.API_PREFIX}/users/", headers=headers)
    assert response.status_code == 200
    users = user.UserResponse(**response.json()[0])
    assert users.email == email
    assert hasattr(users, "id")
    assert hasattr(users, "created_at")
