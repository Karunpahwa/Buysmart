import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, ForeignKey, Text, Enum, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.main import app
from app.database import get_db
from app.services.auth import create_user, create_access_token
from app.models.schemas import UserCreate
import enum
from datetime import datetime
import uuid

# Remove TestBase, TestUser, TestRequirement, TestListing, and related test enums

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
    from app.models.database import Base
    Base.metadata.create_all(bind=engine)

def teardown_module():
    from app.models.database import Base
    Base.metadata.drop_all(bind=engine)

def get_test_token_and_requirement():
    db = TestingSessionLocal()
    unique_email = f"listingtest_{uuid.uuid4()}@example.com"
    user_data = UserCreate(email=unique_email, password="testpassword")
    user = create_user(db, user_data)
    user.id = str(user.id)
    token = create_access_token(data={"sub": user.email})
    requirement_id = str(uuid.uuid4())
    user_id = str(user.id)
    from app.models.database import Requirement, Category, RequirementStatus, RequirementTimeline
    requirement = Requirement(
        id=requirement_id,
        user_id=user_id,
        product_query="Test Product",
        category=Category.ELECTRONICS.value,
        budget_min=100,
        budget_max=200,
        timeline=RequirementTimeline.FLEXIBLE.value,
        status=RequirementStatus.ACTIVE.value,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(requirement)
    db.commit()
    db.expire_all()
    db.close()
    return token, requirement_id

def test_create_listing():
    token, requirement_id = get_test_token_and_requirement()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "requirement_id": requirement_id,
        "olx_id": "olx123",
        "title": "Test Listing",
        "price": 150,
        "location": "Mumbai",
        "posted_date": "2024-06-01T12:00:00Z"
    }
    response = client.post("/api/listings/", json=data, headers=headers)
    assert response.status_code == 200
    listing = response.json()
    assert listing["title"] == "Test Listing"
    assert listing["olx_id"] == "olx123"

def test_get_listings_for_requirement():
    token, requirement_id = get_test_token_and_requirement()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/listings/{requirement_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "listings" in data
    assert "total" in data

def test_get_listing():
    token, requirement_id = get_test_token_and_requirement()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a listing
    data = {
        "requirement_id": requirement_id,
        "olx_id": "olx456",
        "title": "Single Listing",
        "price": 180,
        "location": "Delhi",
        "posted_date": "2024-06-01T12:00:00Z"
    }
    create_resp = client.post("/api/listings/", json=data, headers=headers)
    listing_id = create_resp.json()["id"]
    # Fetch it
    response = client.get(f"/api/listings/item/{listing_id}", headers=headers)
    assert response.status_code == 200
    listing = response.json()
    assert listing["title"] == "Single Listing"
    assert listing["olx_id"] == "olx456"

def test_update_listing():
    token, requirement_id = get_test_token_and_requirement()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a listing
    data = {
        "requirement_id": requirement_id,
        "olx_id": "olx789",
        "title": "Old Title",
        "price": 200,
        "location": "Bangalore",
        "posted_date": "2024-06-01T12:00:00Z"
    }
    create_resp = client.post("/api/listings/", json=data, headers=headers)
    listing_id = create_resp.json()["id"]
    # Update it
    update_data = {"title": "Updated Title", "price": 210}
    response = client.patch(f"/api/listings/item/{listing_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    listing = response.json()
    assert listing["title"] == "Updated Title"
    assert listing["price"] == 210

def test_delete_listing():
    token, requirement_id = get_test_token_and_requirement()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a listing
    data = {
        "requirement_id": requirement_id,
        "olx_id": "olx999",
        "title": "Delete Me",
        "price": 300,
        "location": "Chennai",
        "posted_date": "2024-06-01T12:00:00Z"
    }
    create_resp = client.post("/api/listings/", json=data, headers=headers)
    listing_id = create_resp.json()["id"]
    # Delete it
    response = client.delete(f"/api/listings/item/{listing_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Listing deleted successfully" 