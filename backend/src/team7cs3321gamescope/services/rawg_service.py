import requests
import re
from team7cs3321gamescope.core.config import RAWG_API_KEY

RAWG_BASE_URL = "https://api.rawg.io/api"


def search_for_steam_game_by_name(query: str):
    if not RAWG_API_KEY:
        return {
            "status_code": 500,
            "error": "RAWG_API_KEY is missing from .env",
        }

    if not query or not query.strip():
        return {
            "status_code": 400,
            "error": "Query parameter is required",
        }
    # Search RAWG
    url = f"{RAWG_BASE_URL}/games"
    params = {
        "key": RAWG_API_KEY,
        "search": query.strip(),
        "page_size": 5,     #check a few results to make sure we find the Steam match
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {
            "status_code": 504,
            "error": "Request to RAWG timed out",
        }
    except requests.exceptions.ConnectionError:
        return {
            "status_code": 503,
            "error": "Could not connect to RAWG",
        }
    except requests.exceptions.HTTPError:
        return {
            "status_code": response.status_code,
            "error": "RAWG returned an HTTP error",
            "details": response.text,
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 500,
            "error": "Unexpected RAWG request error",
            "details": str(e),
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "status_code": 502,
            "error": "RAWG returned invalid JSON",
        }
    
    results = data.get("results", [])
    if not results:
        return {
            "status_code": 404,
            "error": "No game found"
        }

    # Find first game that exists on Steam
    selected_game = None
    steam_app_id = None
    steam_url = None

    for game in results:
        rawg_id = game.get("id")

        steam_info = find_steam_info_from_rawg_id(rawg_id)
        if not steam_info:
            continue

        selected_game = game
        steam_app_id = steam_info["app_id"]
        steam_url = steam_info["steam_url"]
        break
    if not selected_game:
        return {
                "status_code": 404,
                "error": "No Steam game found for this query"
        }

    # Assemble full game details
    rawg_id = selected_game.get("id")
    details_url = f"{RAWG_BASE_URL}/games/{rawg_id}"
    params = {"key": RAWG_API_KEY}
    try: 
        response = requests.get(details_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return { 
                "status_code": 500,
                "error": "Failed to fetch game details",
        } 
    try: 
        details = response.json()
    except ValueError:
        return {
                "status_code": 502,
                "error": "Invalid JSON from RAWG"
        }
    return {
        "status_code": 200,
        "game": {
            "name": details.get("name"),
            "release_date": details.get("released"),
            "rating": details.get("rating"),
            "genres": [g["name"] for g in details.get("genres", [])],
            "description": details.get("description_raw") or details.get("description"),
            "publishers": [p["name"] for p in details.get("publishers", [])],
            "tags": [t["name"] for t in details.get("tags", [])],
            "steam_app_id": steam_app_id,
            "steam_url": steam_url,
        }, 
    }

def find_steam_info_from_rawg_id(rawg_id: int):
    stores_result = get_game_store_links(rawg_id)
    if stores_result.get("status_code") != 200:
        return None

    for store_entry in stores_result.get("results", []):
        store_name = (store_entry.get("store_name") or "").lower()
        store_domain = (store_entry.get("store_domain") or "").lower()
        store_url = store_entry.get("url")

        is_steam = (
            "steam" in store_name
            or "steampowered.com" in store_domain
            or ("steam" in (store_url or "").lower())
        )

        if not is_steam:
            continue

        app_id = extract_steam_app_id_from_url(store_url)
        if app_id:
            return {
                "app_id": app_id,
                "steam_url": store_url,
            }

    return None

def get_game_store_links(rawg_game_id: int):
    if not RAWG_API_KEY:
        return {
            "status_code": 500,
            "error": "RAWG_API_KEY is missing from .env",
        }

    if rawg_game_id is None:
        return {
            "status_code": 400,
            "error": "RAWG game ID is required",
        }

    url = f"{RAWG_BASE_URL}/games/{rawg_game_id}/stores"
    params = {
        "key": RAWG_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {
            "status_code": 504,
            "error": "Request to RAWG timed out",
        }
    except requests.exceptions.ConnectionError:
        return {
            "status_code": 503,
            "error": "Could not connect to RAWG",
        }
    except requests.exceptions.HTTPError:
        return {
            "status_code": response.status_code,
            "error": "RAWG returned an HTTP error",
            "details": response.text,
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 500,
            "error": "Unexpected RAWG request error",
            "details": str(e),
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "status_code": 502,
            "error": "RAWG returned invalid JSON",
        }

    simplified_results = []
    for store_entry in data.get("results", []):
        store = store_entry.get("store", {})
        simplified_results.append(
            {
                "store_name": store.get("name"),
                "store_domain": store.get("domain"),
                "url": store_entry.get("url"),
            }
        )

    return {
        "status_code": 200,
        "results": simplified_results,
    }

def extract_steam_app_id_from_url(url: str):
    if not url:
        return None

    match = re.search(r"/app/(\d+)", url)
    if match:
        return match.group(1)

    match = re.search(r"[?&]appid=(\d+)", url)
    if match:
        return match.group(1)

    return None
