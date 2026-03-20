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

    response = requests.get(url, params=params, timeout=10)

    return {
        "status_code": response.status_code,
        "data": response.json(),
    }
