import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.db.database import SessionLocal, engine, Base
from app.api.v1.schemas.user import UserRegisterCreate, UserLogin
from app.api.v1.models.user import User
from app.api.core.security import hash_password
import random
import string

def generate_unique_email(base_email):
    """Generate a unique email address for each test."""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base_email.split('@')[0]}_{random_suffix}@{base_email.split('@')[1]}"


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    client = TestClient(app)
    yield client
    
    db.query(User).delete()  
    db.commit()
    db.close()
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(client):
    db = SessionLocal()
    user_data = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "phone_number": "1234567890",
        "password": "password123"
    }
    hashed_password = hash_password(user_data["password"])
    user = User(
        full_name=user_data["full_name"],
        email=user_data["email"],
        password=hashed_password,
        phone_number=user_data["phone_number"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_register(client):
    unique_email = generate_unique_email("newuser@example.com")
    user_data = {
        "full_name": "New User",
        "email": unique_email,
        "phone_number": "0987654321",
        "password": "password123"
    }
    
    response = client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["full_name"] == user_data["full_name"]
    assert "id" in response.json()

def test_register_duplicate_email(client, test_user):
    user_data = {
        "full_name": "Another User",
        "email": test_user.email,
        "phone_number": "1231231234",
        "password": "password123"
    }
    
    response = client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
