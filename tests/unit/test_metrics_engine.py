from backend.services.metrics_engine import calculate_performance

def test_calculate_roas_correctly(sample_campaign_data):
    """
    Test that ROAS is calculated correctly (Revenue / Spend).
    """
    # Execute the function with data from conftest.py
    result = calculate_performance(sample_campaign_data)
    
    # Verify Facebook (Spend 100, Rev 200 -> ROAS 2.0)
    fb_metrics = next(r for r in result.summary if r.channel == "Facebook")
    assert fb_metrics.roas == 2.0
    assert fb_metrics.recommendation_status == "Good"

def test_calculate_bad_performance(sample_campaign_data):
    """
    Test that it detects bad campaigns (ROAS < 1).
    """
    # Verify Google (Spend 200, Rev 100 -> ROAS 0.5)
    result = calculate_performance(sample_campaign_data)
    google_metrics = next(r for r in result.summary if r.channel == "Google")
    assert google_metrics.roas == 0.5
    assert google_metrics.recommendation_status == "Critical"

def test_empty_data():
    """
    Test that the system does not explode if we pass an empty list.
    """
    result = calculate_performance([])
    assert result.global_roas == 0.0
    assert len(result.summary) == 0