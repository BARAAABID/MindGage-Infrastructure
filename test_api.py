import uuid
from fastapi.testclient import TestClient
from main import app

# Create a simulated browser that bypasses Uvicorn entirely
client = TestClient(app)

def test_valid_checkin_submission():
    """Test that the API accepts perfect data and returns a 200 OK."""
    valid_payload = {
        "checkin_id": f"test_{uuid.uuid4()}",  # Generates a random ID every time!
        "user_id": "test_user",
        "timestamp": "2026-08-20T20:26:46Z",
        "mood": "Focused",
        "energy_level": 4,     
        "focus_level": 5,      
        "stress_level": 3,
        "sleep_quality": "Good",
        "physical_comfort": "Comfortable",
        "excitement_to_work": 4,
        "notes": "Testing the pipeline"
    }
    
    response = client.post("/checkins/test_user", json=valid_payload)
    assert response.status_code == 200

def test_invalid_checkin_blocked():
    """Test that the API properly blocks bad data and throws a 422 Error."""
    invalid_payload = {
        "checkin_id": f"test_{uuid.uuid4()}",
        "user_id": "test_user",
        "timestamp": "2026-08-20T20:26:46Z",
        "mood": "Hyper",
        "energy_level": 9,     # INVALID (Over 5)
        "focus_level": 5,
        "stress_level": 3,
        "sleep_quality": "Good",
        "physical_comfort": "Comfortable",
        "excitement_to_work": 4,
        "notes": "Trying to break the system"
    }
    
    response = client.post("/checkins/test_user", json=invalid_payload)
    
    # We WANT this to fail, so asserting 422 means the test PASSES
    assert response.status_code == 422
    assert "Input should be less than or equal to 5" in response.text