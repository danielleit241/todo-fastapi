import pytest
from starlette.testclient import TestClient
from app.main import app
from app.database import Base
from tests.database import engine, override_get_db
from app.database import get_db
from app.config import settings

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    Create a new database for the test, yield a TestClient, and drop the database after the test.
    """
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def create_user(client):
    def _create_user(email="test@example.com", password="testpassword"):
        user_data = {"email": email, "password": password}
        response = client.post(f"{settings.API_PREFIX}/users/", json=user_data)
        assert response.status_code == 201
        return response.json()
    return _create_user

@pytest.fixture(scope="function")
def login_user(client, create_user):
    def _login_user(email="test@example.com", password="testpassword"):
        create_user(email=email, password=password)
        response = client.post(f"{settings.API_PREFIX}/auth/login/", data={
            "username": email,
            "password": password
        })
        assert response.status_code == 200
        return response.json()
    return _login_user

@pytest.fixture(scope="function")
def create_token(client, login_user):
    def _create_token(email="test@example.com", password="testpassword"):
        token_data = login_user(email=email, password=password)
        return token_data
    return _create_token

@pytest.fixture(scope="function")
def authorized_client(client, create_token):
    def _authorized_client(email="test@example.com", password="testpassword"):
        token = create_token(email=email, password=password)
        headers = {
            "Authorization": f"Bearer {token['access_token']}"
        }
        return client, headers
    return _authorized_client