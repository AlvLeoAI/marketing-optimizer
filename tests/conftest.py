import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.schemas import CampaignRecord
from datetime import date

# --- API CLIENT (For Integration Tests) ---
@pytest.fixture
def client():
    """
    Creates a simulated test client for the API.
    Allows making requests without spinning up the actual server.
    
    """
    return TestClient(app)

# --- SAMPLE DATA (For Unit Tests) ---
@pytest.fixture
def sample_campaign_data():
    """
    Generates a list of valid CampaignRecord objects for testing.
    """
    return [
        CampaignRecord(
            date=date(2024, 1, 1),
            channel="Facebook",
            campaign_name="Test_Camp_1",
            spend=100.0,
            revenue=200.0, # ROAS = 2.0
            clicks=50,
            conversions=5
        ),
        CampaignRecord(
            date=date(2024, 1, 1),
            channel="Google",
            campaign_name="Test_Camp_2",
            spend=200.0,
            revenue=100.0, # ROAS = 0.5
            clicks=100,
            conversions=2
        )
    ]