import pytest
import json
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ping():
    """Test health check endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_create_user():
    """Test user creation"""
    user_data = {"name": "Test User"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["points"] == 0
    assert data["rank"] == "Bronze"
    assert data["donations_count"] == 0
    return data["id"]

def test_donate():
    """Test donation endpoint"""
    # Create user first
    user_response = client.post("/users/", json={"name": "Donor User"})
    user_id = user_response.json()["id"]
    
    # Make donation
    donation_data = {
        "user_id": user_id,
        "item_type": "food",
        "location": "Test City"
    }
    response = client.post("/donate", json=donation_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["user_id"] == user_id
    assert data["points_awarded"] == 150  # 100 * 1.5 urgency * 1.0 frequency
    assert data["total_points"] == 150

def test_frequency_bonus():
    """Test frequency bonus calculation"""
    # Create user
    user_response = client.post("/users/", json={"name": "Frequent Donor"})
    user_id = user_response.json()["id"]
    
    # Make 5 donations to trigger frequency bonus
    for i in range(5):
        donation_data = {
            "user_id": user_id,
            "item_type": "clothing",
            "location": f"Location {i}"
        }
        client.post("/donate", json=donation_data)
    
    # 6th donation should have frequency bonus
    donation_data = {
        "user_id": user_id,
        "item_type": "clothing",
        "location": "Final Location"
    }
    response = client.post("/donate", json=donation_data)
    data = response.json()
    
    # Points should be 132 (100 * 1.2 urgency * 1.1 frequency)
    assert data["points_awarded"] == 132

def test_get_user_donations():
    """Test getting user donations"""
    # Create user and make donation
    user_response = client.post("/users/", json={"name": "History User"})
    user_id = user_response.json()["id"]
    
    client.post("/donate", json={
        "user_id": user_id,
        "item_type": "books",
        "location": "Library"
    })
    
    # Get donations
    response = client.get(f"/donations/user/{user_id}")
    assert response.status_code == 200
    donations = response.json()
    assert len(donations) == 1
    assert donations[0]["item_type"] == "books"
    assert donations[0]["location"] == "Library"

if __name__ == "__main__":
    # Run tests
    test_ping()
    print("✓ Ping test passed")
    
    test_create_user()
    print("✓ User creation test passed")
    
    test_donate()
    print("✓ Donation test passed")
    
    test_frequency_bonus()
    print("✓ Frequency bonus test passed")
    
    test_get_user_donations()
    print("✓ User donations test passed")
    
    print("\nAll tests passed! ✨")
