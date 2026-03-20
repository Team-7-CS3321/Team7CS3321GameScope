import requests
from app.core.config import RAWG_API_KEY

RAWG_BASE_URL = "https://api.rawg.io/api"


def search_games(query: str):
    if not RAWG_API_KEY:
        return {"error": "RAWG_API_KEY is missing from .env"}

    url = f"{RAWG_BASE_URL}/games"
    params = {
        "key": RAWG_API_KEY,
        "search": query,
        "page_size": 5,
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    simplified_results = []
    for game in data.get("results", []):
        simplified_results.append({
            "id": game.get("id"),
            "name": game.get("name"),
            "slug": game.get("slug"),
            "released": game.get("released"),
            "rating": game.get("rating"),
            "metacritic": game.get("metacritic"),
            "platforms": [
                p["platform"]["name"]
                for p in game.get("platforms", [])
                if "platform" in p and "name" in p["platform"]
            ],
            "stores": [
                s["store"]["name"]
                for s in game.get("stores", [])
                if "store" in s and "name" in s["store"]
            ],
        })

    return {
        "status_code": response.status_code,
        "count": data.get("count"),
        "results": simplified_results,
    }
