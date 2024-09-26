from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

# Test Admin user login
@pytest.fixture(scope="module")
def test_login_otp():
    response = client.post("/api/v1/login/otp", data={"username": "admin@example.com", "password": "123456789"})
    otp = response.json().get("otp")
    assert response.status_code == 200
    assert otp is not None
    return otp

# Test Enter OTP and get access token
@pytest.fixture(scope="module")
def test_login_access_token(test_login_otp):
    response = client.post("/api/v1/login/access-token", json={"email": "admin@example.com", "otp": test_login_otp})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert "token_type" in response.json()
    token = response.json().get("access_token")
    return token

# Test Get All Users
def test_get_all_users(test_login_access_token):
    response = client.get("/api/v1/users/get-all", headers={"Authorization": f"Bearer {test_login_access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test Create New User
def test_create_new_user(test_login_access_token):
    new_user = {"email": "newtestuser@example.com", "password": "new_password", "role_id": 2}
    response = client.post(
        "/api/v1/users/create",
        json=new_user,
        headers={"Authorization": f"Bearer {test_login_access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newtestuser@example.com"

# Test Reset Password
def test_reset_password(test_login_access_token):
    current_password = "123456789"
    new_password = "123456789"
    response = client.post(
        "/api/v1/login/reset-password",
        json={"email": "admin@example.com", "current_password": current_password, "new_password": new_password},
        headers={"Authorization": f"Bearer {test_login_access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"
