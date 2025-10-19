import pytest
from app.schemas import token, user
from app.config import settings

@pytest.mark.parametrize("email, password", [
    ("test@example.com", "SecureP@ssw0rd!"),
    ("user@example.com", "AnotherP@ssw0rd!"),
    ("admin@example.com", "AdminP@ssw0rd!")
])
def test_create_user_success_with_response_201(client, email, password):
    """Test creating a new user via API."""
    user_data = {
        "email": email,
        "password": password
    }

    response = client.post(f"{settings.API_PREFIX}/users/", json=user_data)
    assert response.status_code == 201
    test_create_user = user.UserResponse(**response.json())
    assert test_create_user.email == user_data["email"]
    assert hasattr(test_create_user, "id")
    assert hasattr(test_create_user, "created_at")
    assert not hasattr(test_create_user, "password")  # Ensure password is not returned
    assert not hasattr(test_create_user, "hashed_password")  # Ensure hashed password is not returned

@pytest.mark.parametrize("email, password", [
        ("test@example.com", "SecureP@ssw0rd!"),
        ("user@example.com", "AnotherP@ssw0rd!"),
        ("admin@example.com", "AdminP@ssw0rd!")
])
def test_create_user_failure_with_email_exists_with_response_400(client, email, password):
    """Test creating a new user with an email that already exists."""
    existing_user_data = {
        "email": email,
        "password": password
    }

    response1 = client.post(f"{settings.API_PREFIX}/users/", json=existing_user_data)
    assert response1.status_code == 201

    response2 = client.post(f"{settings.API_PREFIX}/users/", json=existing_user_data)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"


@pytest.mark.parametrize("email, password", [
    ("test@example.com", "SecureP@ssw0rd!"),
    ("user@example.com", "AnotherP@ssw0rd!"),
    ("admin@example.com", "AdminP@ssw0rd!")
])
def test_login_user_success_with_response_200(client, email, password):
    """Test logging in a user via API."""
    user_data_create = {
        "email": email,
        "password": password
    }
    client.post(f"{settings.API_PREFIX}/users/", json=user_data_create)
    response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
        "username": user_data_create["email"],
        "password": user_data_create["password"]
    })
    assert response.status_code == 200
    token_response = token.Token(**response.json())
    assert token_response.token_type == "bearer"
    assert token_response.access_token is not None

@pytest.mark.parametrize("email, password", [
    ("invalid@example.com", "WrongP@ssw0rd!")
])
def test_login_user_failure_with_unregistered_email_with_response_403(client, email, password):
    """Test logging in a user with invalid credentials."""
    user_data_create = {
        "email": email,
        "password": password
    }
    response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
        "username": user_data_create["email"],
        "password": user_data_create["password"]
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"

def test_login_user_failure_with_wrong_password_email_with_response_403(client):
    """Test logging in a user with wrong password."""
    user_data_create = {
        "email": "w@example.com",
        "password": "CorrectP@ssw0rd!"
    }
    client.post(f"{settings.API_PREFIX}/users/", json=user_data_create)
    response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
        "username": user_data_create["email"],
        "password": "WrongP@ssw0rd!"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"

@pytest.mark.parametrize("email, password", [
    ("test@example.com", "SecureP@ssw0rd!"),
    ("user@example.com", "AnotherP@ssw0rd!"),
    ("admin@example.com", "AdminP@ssw0rd!")
])
def test_get_all_users_success_with_response_200(client, email, password):
    """Test retrieving all users via API."""
    user_data = {
        "email": email,
        "password": password
    }
    client.post(f"{settings.API_PREFIX}/users/", json=user_data)
    login_response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })
    token = login_response.json()["access_token"]
    headers = {
            "Authorization": f"Bearer {token}"
        }
    response = client.get(f"{settings.API_PREFIX}/users/", headers=headers)
    assert response.status_code == 200
    users = user.UserResponse(**response.json()[0])
    assert users.email == user_data["email"]
    assert hasattr(users, "id")
    assert hasattr(users, "created_at")
