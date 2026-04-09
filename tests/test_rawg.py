from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rawg_search_success():
    mock_result = {
        "status_code": 200,
        "game": {
            "name": "Elden Ring",
            "release_date": "2022-02-25",
            "rating": 4.5,
            "steam_app_id": "1245620",
            "steam_url": "https://store.steampowered.com/app/1245620",
            "genres": ["RPG"],
            "tags": ["Souls-like"],
            "publishers": ["Bandai Namco"],
            "description": "An action RPG."
        }
    }
    with patch("app.api.rawg.search_for_steam_game_by_name", return_value=mock_result):
        response = client.get("/rawg/search?query=Elden Ring")
        assert response.status_code == 200
        assert response.json()["data"]["game"]["name"] == "Elden Ring"

def test_rawg_search_no_steam_game_found():
    mock_result = {
        "status_code": 404,
        "error": "No Steam game found for this query"
    }
    with patch("app.api.rawg.search_for_steam_game_by_name", return_value=mock_result):
        response = client.get("/rawg/search?query=somefakegame999")
        assert response.status_code == 404

def test_rawg_search_missing_query():
    response = client.get("/rawg/search")
    assert response.status_code == 422

def test_rawg_search_missing_api_key():
    mock_result = {
        "status_code": 400,
        "error": "Query parameter is required"
    }
    with patch("app.api.rawg.search_for_steam_game_by_name", return_value=mock_result):
        response = client.get("/rawg/search?query=Elden Ring")
        assert response.status_code == 400

def test_rawg_search_timeout():
    mock_result = {
        "status_code": 504,
        "error": "Request to RAWG timed out"
    }
    with patch("app.api.rawg.search_for_steam_game_by_name", return_value=mock_result):
        response = client.get("/rawg/search?query=Elden Ring")
        assert response.status_code == 504

def test_rawg_search_invalid_json():
    mock_result = {
        "status_code": 502,
        "error": "RAWG returned invalid JSON"
    }
    with patch("app.api.rawg.search_for_steam_game_by_name", return_value=mock_result):
        response = client.get("/rawg/search?query=Elden Ring")
        assert response.status_code == 502
