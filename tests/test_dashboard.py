def test_dashboard_contains_qa_metrics(client):
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"QA dashboard" in response.data
    assert b"TOTAL TESTS" in response.data
    assert b"AUTOMATION PASS RATE" in response.data
