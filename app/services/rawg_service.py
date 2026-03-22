import requests
from app.core.config import RAWG_API_KEY

RAWG_BASE_URL = "https://api.rawg.io/api"


def search_games(query: str):
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

    url = f"{RAWG_BASE_URL}/games"
    params = {
        "key": RAWG_API_KEY,
        "search": query.strip(),
        "page_size": 5,
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
    for game in data.get("results", []):
        simplified_results.append(
            {
                "id": game.get("id"),
                "name": game.get("name"),
                "slug": game.get("slug"),
                "released": game.get("released"),
                "rating": game.get("rating"),
                "metacritic": game.get("metacritic"),
                "platforms": [
                    platform["platform"]["name"]
                    for platform in game.get("platforms", [])
                    if "platform" in platform and "name" in platform["platform"]
                ],
                "stores": [
                    store["store"]["name"]
                    for store in game.get("stores", [])
                    if "store" in store and "name" in store["store"]
                ],
            }
        )

    return {
        "status_code": 200,
        "count": data.get("count", 0),
        "results": simplified_results,
    }
