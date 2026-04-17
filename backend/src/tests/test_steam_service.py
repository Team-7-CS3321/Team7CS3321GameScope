from unittest.mock import patch, MagicMock
import requests
from team7cs3321gamescope.services.steam_service import (
    get_game_achievements,
    get_global_achievement_percentages,
    get_achievements_with_rarity,
)

# --- get_game_achievements ---

def test_get_game_achievements_missing_api_key():
    with patch("team7cs3321gamescope.services.steam_service.STEAM_API_KEY", ""):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 500

def test_get_game_achievements_missing_app_id():
    result = get_game_achievements("")
    assert result["status_code"] == 400

def test_get_game_achievements_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "game": {
            "gameName": "Elden Ring",
            "gameVersion": "1",
            "availableGameStats": {
                "achievements": [
                    {
                        "name": "ACH1",
                        "displayName": "First Kill",
                        "description": "Kill something",
                        "hidden": 0,
                        "icon": "http://icon.url"
                    }
                ]
            }
        }
    }
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 200
        assert result["game_name"] == "Elden Ring"
        assert len(result["achievements"]) == 1
        assert result["achievements"][0]["name"] == "ACH1"

def test_get_game_achievements_no_game_schema():
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 404

def test_get_game_achievements_timeout():
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 504

def test_get_game_achievements_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 503

def test_get_game_achievements_http_error():
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mock_response
    )
    with patch("requests.get", return_value=mock_response):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 403

def test_get_game_achievements_invalid_json():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.side_effect = ValueError("No JSON")
    with patch("requests.get", return_value=mock_response):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 502

def test_get_game_achievements_empty_achievements():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "game": {
            "gameName": "Some Game",
            "gameVersion": "1",
            "availableGameStats": {
                "achievements": []
            }
        }
    }
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        result = get_game_achievements("1245620")
        assert result["status_code"] == 200
        assert result["achievements"] == []

# --- get_global_achievement_percentages ---

def test_get_global_percentages_missing_app_id():
    result = get_global_achievement_percentages("")
    assert result["status_code"] == 400

def test_get_global_percentages_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "achievementpercentages": {
            "achievements": [
                {"name": "ACH1", "percent": 21.5}
            ]
        }
    }
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        result = get_global_achievement_percentages("1245620")
        assert result["status_code"] == 200
        assert len(result["achievement_percentages"]) == 1
        assert result["achievement_percentages"][0]["percent"] == 21.5

def test_get_global_percentages_timeout():
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result = get_global_achievement_percentages("1245620")
        assert result["status_code"] == 504

def test_get_global_percentages_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        result = get_global_achievement_percentages("1245620")
        assert result["status_code"] == 503

def test_get_global_percentages_invalid_json():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.side_effect = ValueError("No JSON")
    with patch("requests.get", return_value=mock_response):
        result = get_global_achievement_percentages("1245620")
        assert result["status_code"] == 502

def test_get_global_percentages_http_error():
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mock_response
    )
    with patch("requests.get", return_value=mock_response):
        result = get_global_achievement_percentages("1245620")
        assert result["status_code"] == 403

# --- get_achievements_with_rarity ---

def test_get_achievements_with_rarity_success():
    mock_achievements = {
        "status_code": 200,
        "game_name": "Elden Ring",
        "game_version": "1",
        "achievements": [
            {
                "name": "ACH1",
                "display_name": "First Kill",
                "description": "Kill something",
                "hidden": 0,
                "icon": "http://icon.url"
            }
        ]
    }
    mock_percentages = {
        "status_code": 200,
        "achievement_percentages": [
            {"name": "ACH1", "percent": 21.5}
        ]
    }
    with patch("team7cs3321gamescope.services.steam_service.get_game_achievements", return_value=mock_achievements):
        with patch("team7cs3321gamescope.services.steam_service.get_global_achievement_percentages", return_value=mock_percentages):
            result = get_achievements_with_rarity("1245620")
            assert result["status_code"] == 200
            assert result["achievements"][0]["global_percentage"] == 21.5

def test_get_achievements_with_rarity_achievements_fail():
    mock_fail = {"status_code": 504, "error": "Timeout"}
    with patch("team7cs3321gamescope.services.steam_service.get_game_achievements", return_value=mock_fail):
        result = get_achievements_with_rarity("1245620")
        assert result["status_code"] == 504

def test_get_achievements_with_rarity_percentages_fail():
    mock_achievements = {
        "status_code": 200,
        "game_name": "Elden Ring",
        "game_version": "1",
        "achievements": []
    }
    mock_fail = {"status_code": 503, "error": "Connection error"}
    with patch("team7cs3321gamescope.services.steam_service.get_game_achievements", return_value=mock_achievements):
        with patch("team7cs3321gamescope.services.steam_service.get_global_achievement_percentages", return_value=mock_fail):
            result = get_achievements_with_rarity("1245620")
            assert result["status_code"] == 503

def test_get_achievements_with_rarity_percentage_not_matched():
    mock_achievements = {
        "status_code": 200,
        "game_name": "Elden Ring",
        "game_version": "1",
        "achievements": [
            {"name": "ACH1", "display_name": "First Kill", "description": "", "hidden": 0, "icon": ""}
        ]
    }
    mock_percentages = {
        "status_code": 200,
        "achievement_percentages": []
    }
    with patch("team7cs3321gamescope.services.steam_service.get_game_achievements", return_value=mock_achievements):
        with patch("team7cs3321gamescope.services.steam_service.get_global_achievement_percentages", return_value=mock_percentages):
            result = get_achievements_with_rarity("1245620")
            assert result["status_code"] == 200
            assert result["achievements"][0]["global_percentage"] is None
