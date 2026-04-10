import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- Route Tests ---

def test_achievements_success():
    mock_result = {
        "status_code": 200,
        "game_name": "Elden Ring",
        "game_version": "1",
        "achievements": [
            {"name": "ACH1", "display_name": "First Kill", "global_percentage": 80.0}
        ]
    }
    with patch("app.api.steam.get_achievements_with_rarity", return_value=mock_result):
        response = client.get("/steam/achievements?app_id=1245620")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["game_name"] == "Elden Ring"
        assert len(data["data"]["achievements"]) == 1

def test_achievements_missing_app_id():
    response = client.get("/steam/achievements")
    assert response.status_code == 422  # FastAPI validation error

def test_achievements_timeout():
    mock_result = {
        "status_code": 504,
        "error": "Request to Steam timed out"
    }
    with patch("app.api.steam.get_achievements_with_rarity", return_value=mock_result):
        response = client.get("/steam/achievements?app_id=1245620")
        assert response.status_code == 504

def test_achievements_connection_error():
    mock_result = {
        "status_code": 503,
        "error": "Could not connect to Steam"
    }
    with patch("app.api.steam.get_achievements_with_rarity", return_value=mock_result):
        response = client.get("/steam/achievements?app_id=1245620")
        assert response.status_code == 503

def test_achievements_missing_api_key():
    mock_result = {
        "status_code": 500,
        "error": "STEAM_API_KEY is missing from .env"
    }
    with patch("app.api.steam.get_achievements_with_rarity", return_value=mock_result):
        response = client.get("/steam/achievements?app_id=1245620")
        assert response.status_code == 500
