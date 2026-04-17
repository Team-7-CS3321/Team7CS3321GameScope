from unittest.mock import patch
from fastapi.testclient import TestClient
from team7cs3321gamescope.main import app

client = TestClient(app)

def test_full_report_success():
    mock_result = {
        "status_code": 200,
        "game": {
            "name": "Elden Ring",
            "release_date": "2022-02-25",
            "rating": 4.5,
            "genres": ["RPG"],
            "tags": ["Souls-like"],
            "publishers": ["Bandai Namco"],
            "description": "An action RPG.",
            "steam_app_id": "1245620",
            "steam_url": "https://store.steampowered.com/app/1245620",
            "achievement_count": 1,
            "difficulty_score": 78.5,
            "achievements": [
                {"name": "ACH1", "display_name": "First Kill", "global_percentage": 21.5}
            ]
        }
    }
    with patch("team7cs3321gamescope.api.combined.get_full_report", return_value=mock_result):
        response = client.get("/report/?game_name=Elden Ring")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["game"]["name"] == "Elden Ring"
        assert data["data"]["game"]["difficulty_score"] == 78.5

def test_full_report_game_not_found():
    mock_result = {
        "status_code": 404,
        "error": "No Steam game found for this query"
    }
    with patch("team7cs3321gamescope.api.combined.get_full_report", return_value=mock_result):
        response = client.get("/report/?game_name=fakegame999")
        assert response.status_code == 404

def test_full_report_no_steam_id():
    mock_result = {
        "status_code": 404,
        "error": "Steam app ID not found for this game"
    }
    with patch("team7cs3321gamescope.api.combined.get_full_report", return_value=mock_result):
        response = client.get("/report/?game_name=somegame")
        assert response.status_code == 404

def test_full_report_missing_game_name():
    response = client.get("/report/")
    assert response.status_code == 422

def test_full_report_steam_error():
    mock_result = {
        "status_code": 503,
        "error": "Could not connect to Steam"
    }
    with patch("team7cs3321gamescope.api.combined.get_full_report", return_value=mock_result):
        response = client.get("/report/?game_name=Elden Ring")
        assert response.status_code == 503

def test_full_report_no_achievements():
    mock_result = {
        "status_code": 200,
        "game": {
            "name": "Some Game",
            "achievement_count": 0,
            "difficulty_score": 0,
            "achievements": []
        }
    }
    with patch("team7cs3321gamescope.api.combined.get_full_report", return_value=mock_result):
        response = client.get("/report/?game_name=Some Game")
        assert response.status_code == 200
        assert response.json()["data"]["game"]["difficulty_score"] == 0
