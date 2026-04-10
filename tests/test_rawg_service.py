from unittest.mock import patch, MagicMock, call
import requests
from app.services.rawg_service import (
    search_for_steam_game_by_name,
    find_steam_info_from_rawg_id,
    get_game_store_links,
    extract_steam_app_id_from_url,
)

# --- extract_steam_app_id_from_url ---

def test_extract_steam_app_id_standard_url():
    url = "https://store.steampowered.com/app/1245620/Elden_Ring/"
    assert extract_steam_app_id_from_url(url) == "1245620"

def test_extract_steam_app_id_query_param():
    url = "https://store.steampowered.com/?appid=1245620"
    assert extract_steam_app_id_from_url(url) == "1245620"

def test_extract_steam_app_id_no_match():
    url = "https://www.epicgames.com/store/en-US/"
    assert extract_steam_app_id_from_url(url) is None

def test_extract_steam_app_id_none_url():
    assert extract_steam_app_id_from_url(None) is None

def test_extract_steam_app_id_empty_url():
    assert extract_steam_app_id_from_url("") is None

# --- get_game_store_links ---

def test_get_game_store_links_missing_api_key():
    with patch("app.services.rawg_service.RAWG_API_KEY", ""):
        result = get_game_store_links(12345)
        assert result["status_code"] == 500

def test_get_game_store_links_missing_id():
    result = get_game_store_links(None)
    assert result["status_code"] == 400

def test_get_game_store_links_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "store": {"name": "Steam", "domain": "steampowered.com"},
                "url": "https://store.steampowered.com/app/1245620"
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    with patch("requests.get", return_value=mock_response):
        result = get_game_store_links(12345)
        assert result["status_code"] == 200
        assert result["results"][0]["store_name"] == "Steam"

def test_get_game_store_links_timeout():
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result = get_game_store_links(12345)
        assert result["status_code"] == 504

def test_get_game_store_links_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        result = get_game_store_links(12345)
        assert result["status_code"] == 503

def test_get_game_store_links_invalid_json():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.side_effect = ValueError("No JSON")
    with patch("requests.get", return_value=mock_response):
        result = get_game_store_links(12345)
        assert result["status_code"] == 502

def test_get_game_store_links_http_error():
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mock_response
    )
    with patch("requests.get", return_value=mock_response):
        result = get_game_store_links(12345)
        assert result["status_code"] == 403

# --- find_steam_info_from_rawg_id ---

def test_find_steam_info_success():
    mock_stores = {
        "status_code": 200,
        "results": [
            {
                "store_name": "Steam",
                "store_domain": "steampowered.com",
                "url": "https://store.steampowered.com/app/1245620"
            }
        ]
    }
    with patch("app.services.rawg_service.get_game_store_links", return_value=mock_stores):
        result = find_steam_info_from_rawg_id(12345)
        assert result is not None
        assert result["app_id"] == "1245620"

def test_find_steam_info_no_steam_store():
    mock_stores = {
        "status_code": 200,
        "results": [
            {
                "store_name": "Epic Games",
                "store_domain": "epicgames.com",
                "url": "https://www.epicgames.com/store/"
            }
        ]
    }
    with patch("app.services.rawg_service.get_game_store_links", return_value=mock_stores):
        result = find_steam_info_from_rawg_id(12345)
        assert result is None

def test_find_steam_info_store_links_fail():
    mock_fail = {"status_code": 500, "error": "Error"}
    with patch("app.services.rawg_service.get_game_store_links", return_value=mock_fail):
        result = find_steam_info_from_rawg_id(12345)
        assert result is None

def test_search_missing_api_key():
    with patch("app.services.rawg_service.RAWG_API_KEY", ""):
        result = search_for_steam_game_by_name("Elden Ring")
        assert result["status_code"] == 500

def test_search_empty_query():
    result = search_for_steam_game_by_name("")
    assert result["status_code"] == 400

def test_search_timeout():
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result = search_for_steam_game_by_name("Elden Ring")
        assert result["status_code"] == 504

def test_search_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        result = search_for_steam_game_by_name("Elden Ring")
        assert result["status_code"] == 503

def test_search_invalid_json():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.side_effect = ValueError("No JSON")
    with patch("requests.get", return_value=mock_response):
        result = search_for_steam_game_by_name("Elden Ring")
        assert result["status_code"] == 502

def test_search_no_results():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"results": []}
    with patch("requests.get", return_value=mock_response):
        result = search_for_steam_game_by_name("fakegame999")
        assert result["status_code"] == 404

def test_search_no_steam_game_found():
    mock_search_response = MagicMock()
    mock_search_response.raise_for_status = MagicMock()
    mock_search_response.json.return_value = {
        "results": [{"id": 999}]
    }
    with patch("requests.get", return_value=mock_search_response):
        with patch("app.services.rawg_service.find_steam_info_from_rawg_id", return_value=None):
            result = search_for_steam_game_by_name("somegame")
            assert result["status_code"] == 404

def test_search_success():
    mock_search_response = MagicMock()
    mock_search_response.raise_for_status = MagicMock()
    mock_search_response.json.return_value = {
        "results": [{"id": 999, "name": "Elden Ring"}]
    }

    mock_details_response = MagicMock()
    mock_details_response.raise_for_status = MagicMock()
    mock_details_response.json.return_value = {
        "name": "Elden Ring",
        "released": "2022-02-25",
        "rating": 4.5,
        "genres": [{"name": "RPG"}],
        "description_raw": "An action RPG.",
        "publishers": [{"name": "Bandai Namco"}],
        "tags": [{"name": "Souls-like"}],
    }

    mock_steam_info = {
        "app_id": "1245620",
        "steam_url": "https://store.steampowered.com/app/1245620"
    }

    with patch("requests.get", side_effect=[mock_search_response, mock_details_response]):
        with patch("app.services.rawg_service.find_steam_info_from_rawg_id", return_value=mock_steam_info):
            result = search_for_steam_game_by_name("Elden Ring")
            assert result["status_code"] == 200
            assert result["game"]["name"] == "Elden Ring"
            assert result["game"]["steam_app_id"] == "1245620"

def test_search_details_fetch_fails():
    mock_search_response = MagicMock()
    mock_search_response.raise_for_status = MagicMock()
    mock_search_response.json.return_value = {
        "results": [{"id": 999, "name": "Elden Ring"}]
    }

    mock_steam_info = {
        "app_id": "1245620",
        "steam_url": "https://store.steampowered.com/app/1245620"
    }

    with patch("requests.get", side_effect=[mock_search_response, requests.exceptions.RequestException]):
        with patch("app.services.rawg_service.find_steam_info_from_rawg_id", return_value=mock_steam_info):
            result = search_for_steam_game_by_name("Elden Ring")
            assert result["status_code"] == 500
