import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
from app import app
from src.services.prediction_service import load_model_and_preprocessor
import pandas as pd
import json


# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)



client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_model():
    """Load model and preprocessor before running tests"""
    load_model_and_preprocessor()

# Test data fixtures
@pytest.fixture
def valid_prediction_data():
    return {
        "age": 12,
        "income": 75000.5,
        "employment_type": "full_time",
        "marital_status": "married",
        "time_spent_on_platform": 210.5,
        "number_of_sessions": 22,
        "fields_filled_percentage": 95.2,
        "previous_year_filing": 0,
        "device_type": "desktop",
        "referral_source": "organic_search"
    }

@pytest.fixture
def invalid_prediction_data():
    return {
        "age": "invalid",  # Should be int
        "income": "invalid",  # Should be float
        "employment_type": "invalid_type",
        "marital_status": "married",
        "time_spent_on_platform": 210.5,
        "number_of_sessions": 22,
        "fields_filled_percentage": 95.2,
        "previous_year_filing": 0,
        "device_type": "desktop",
        "referral_source": "organic_search"
    }

# Test prediction endpoint
def test_predict_valid_data(valid_prediction_data):
    """
    Test prediction with valid data
    """
    response = client.post("/predict", json=valid_prediction_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probability" in response.json()
    assert isinstance(response.json()["prediction"], int)
    assert isinstance(response.json()["probability"], float)

def test_predict_invalid_data(invalid_prediction_data):
    """
    Test prediction with invalid data
    """
    response = client.post("/predict", json=invalid_prediction_data)
    # Validation error
    assert response.status_code == 422  

def test_predict_missing_data():
    """
    Test prediction with missing fields
    """
    
    incomplete_data = {
        "age": 30,
        "income": 75000.5
    }
    response = client.post("/predict", json=incomplete_data)
    # validation error
    assert response.status_code == 422
