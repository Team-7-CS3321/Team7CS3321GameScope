import requests
from app.core.config import STEAM_API_KEY

STEAM_BASE_URL = "https://api.steampowered.com"


def get_player_summary(steam_id: str):
    if not STEAM_API_KEY:
        return {
            "status_code": 500,
            "error": "STEAM_API_KEY is missing from .env",
        }

    if not steam_id or not steam_id.strip():
        return {
            "status_code": 400,
            "error": "Steam ID is required",
        }

    cleaned_steam_id = steam_id.strip()

    url = f"{STEAM_BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": cleaned_steam_id,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {
            "status_code": 504,
            "error": "Request to Steam timed out",
        }
    except requests.exceptions.ConnectionError:
        return {
            "status_code": 503,
            "error": "Could not connect to Steam",
        }
    except requests.exceptions.HTTPError:
        return {
            "status_code": response.status_code,
            "error": "Steam returned an HTTP error",
            "details": response.text,
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 500,
            "error": "Unexpected Steam request error",
            "details": str(e),
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "status_code": 502,
            "error": "Steam returned invalid JSON",
        }

    players = data.get("response", {}).get("players", [])
    if not players:
        return {
            "status_code": 404,
            "error": "No player found for the given Steam ID",
            "player": None,
        }

    player = players[0]

    simplified_player = {
        "steamid": player.get("steamid"),
        "personaname": player.get("personaname"),
        "profileurl": player.get("profileurl"),
        "avatarfull": player.get("avatarfull"),
        "realname": player.get("realname"),
        "loccountrycode": player.get("loccountrycode"),
    }

    return {
        "status_code": 200,
        "player": simplified_player,
    }
