import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_review_endpoint():
    payload = {
        "title": "API Test Review",
        "language": "python",
        "source_type": "paste",
        "file_path": "auth.py",
        "source_code": "def login(user, pw):\n    cursor.execute(f'SELECT * FROM users WHERE u={user}')",
        "min_confidence": 0.60
    }
    response = client.post("/api/v1/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "letter_grade" in data
    assert "risk_level" in data
    assert len(data["issues"]) > 0

def test_evaluation_run_endpoint():
    response = client.post("/api/v1/evaluation/run", json={"mode": "hybrid"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_samples"] >= 10
    assert data["precision"] > 80.0
    assert data["f1_score"] > 80.0

def test_dashboard_stats_endpoint():
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "severity_distribution" in data
