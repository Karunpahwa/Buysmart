import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.database import Base, User
from app.services.auth import create_user, create_access_token
from app.models.schemas import UserCreate
import uuid

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_module():
    Base.metadata.create_all(bind=engine)

def teardown_module():
    Base.metadata.drop_all(bind=engine)

def get_test_token():
    """Helper function to get a test token"""
    db = TestingSessionLocal()
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user_data = UserCreate(email=unique_email, password="testpassword")
    user = create_user(db, user_data)
    token = create_access_token(data={"sub": user.email})
    db.close()
    return token

def test_create_requirement():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/api/requirements/", 
        json={
            "product_query": "iPhone 12",
            "category": "electronics",
            "budget_min": 30000,
            "budget_max": 50000,
            "timeline": "flexible"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_query"] == "iPhone 12"
    assert data["category"] == "electronics"

def test_get_requirements():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/requirements/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "requirements" in data
    assert "total" in data

def test_get_requirements_unauthorized():
    response = client.get("/api/requirements/")
    assert response.status_code == 401

def test_update_requirement():
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a requirement
    create_response = client.post("/api/requirements/", 
        json={
            "product_query": "MacBook Pro",
            "category": "electronics",
            "budget_min": 50000,
            "budget_max": 100000,
            "timeline": "urgent"
        },
        headers=headers
    )
    requirement_id = create_response.json()["id"]
    
    # Then update it
    response = client.patch(f"/api/requirements/{requirement_id}",
        json={"status": "paused"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paused" 