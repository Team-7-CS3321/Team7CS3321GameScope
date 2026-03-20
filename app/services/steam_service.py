import requests
from app.core.config import STEAM_API_KEY

STEAM_BASE_URL = "https://api.steampowered.com"


def get_player_summary(steam_id: str):
    if not STEAM_API_KEY:
        return {"error": "STEAM_API_KEY is missing from .env"}

    url = f"{STEAM_BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steam_id,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        players = data.get("response", {}).get("players", [])
        if not players:
            return {
                "status_code": response.status_code,
                "player": None,
                "error": "No player found",
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
            "status_code": response.status_code,
            "player": simplified_player,
        }

    except Exception as e:
        return {"error": str(e)}
