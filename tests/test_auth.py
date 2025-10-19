import pytest
from app.schemas import user, token
from app.config import settings

@pytest.mark.parametrize("email, password", [
    ("test@example.com", "SecureP@ssw0rd!"),
    ("user@example.com", "AnotherP@ssw0rd!"),
    ("admin@example.com", "AdminP@ssw0rd!")
])
def test_create_user_success_with_response_201(client, create_user, email, password):
    """Test creating a new user via API."""
    
    response = create_user(email=email, password=password)
    test_create_user = user.UserResponse(**response)
    assert test_create_user.email == email
    assert hasattr(test_create_user, "id")
    assert hasattr(test_create_user, "created_at")
    assert not hasattr(test_create_user, "password") 
    assert not hasattr(test_create_user, "hashed_password") 

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
def test_login_user_success_with_response_200(client, login_user, email, password):
    """Test logging in a user via API."""
    token = login_user(email=email, password=password)
    assert token is not None
    assert token["token_type"] == "bearer"
    assert token["access_token"] is not None

@pytest.mark.parametrize("email, password", [
    ("invalid@example.com", "WrongP@ssw0rd!")
])
def test_login_user_failure_with_unregistered_email_with_response_403(client, email, password):
    """Test logging in a user with invalid credentials."""
    response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
        "username": email,
        "password": password
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"

@pytest.mark.parametrize("email, password", [
    ("wrong@example.com", "CorrectP@ssw0rd!")
])
def test_login_user_failure_with_wrong_password_email_with_response_403(client, create_user, email, password):
    """Test logging in a user with wrong password."""
    create_user(email=email, password=password)

    response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
        "username": email,
        "password": "WrongP@ssw0rd!"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"
