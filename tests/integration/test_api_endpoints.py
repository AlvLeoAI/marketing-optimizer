def test_health_check(client):
    """
    Verifies that the server responds to the basic ping.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_upload_csv_endpoint(client):
    """
    Simulates the upload of a real CSV file to the endpoint.
    """
    # Creamos un CSV falso en memoria
    csv_content = """date,channel,spend,revenue,clicks,conversions
2024-01-01,TikTok,50,150,200,10
"""
    files = {"file": ("test.csv", csv_content, "text/csv")}
    
    # Perform the POST request
    response = client.post("/analytics/upload-csv", files=files)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Should have calculated 1 channel (TikTok)
    assert len(data["summary"]) == 1
    assert data["summary"][0]["channel"] == "TikTok"
    assert data["summary"][0]["roas"] == 3.0  # 150/50