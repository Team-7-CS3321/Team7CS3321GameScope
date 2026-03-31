import requests
from app.core.config import STEAM_API_KEY
from app.services.rawg_service import get_steam_app_id_from_game_name

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

def get_game_achievements(app_id: str):
    if not STEAM_API_KEY:
        return {
            "status_code": 500,
            "error": "STEAM_API_KEY is missing from .env",
        }

    if not app_id or not str(app_id).strip():
        return {
            "status_code": 400,
            "error": "App ID is required",
        }

    cleaned_app_id = str(app_id).strip()

    url = f"{STEAM_BASE_URL}/ISteamUserStats/GetSchemaForGame/v2/"
    params = {
        "key": STEAM_API_KEY,
        "appid": cleaned_app_id,
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

    game = data.get("game")
    if not game:
        return {
            "status_code": 404,
            "error": "No game schema found for the given App ID",
            "achievements": None,
        }

    achievements = game.get("availableGameStats", {}).get("achievements", [])

    simplified_achievements = []
    for achievement in achievements:
        simplified_achievements.append({
            "name": achievement.get("name"),
            "display_name": achievement.get("displayName"),
            "description": achievement.get("description"),
            "hidden": achievement.get("hidden"),
            "icon": achievement.get("icon"),
        })

    return {
        "status_code": 200,
        "game_name": game.get("gameName"),
        "game_version": game.get("gameVersion"),
        "achievements": simplified_achievements,
    }


def get_global_achievement_percentages(app_id: str):
    if not app_id or not str(app_id).strip():
        return {
            "status_code": 400,
            "error": "App ID is required",
        }

    cleaned_app_id = str(app_id).strip()

    url = f"{STEAM_BASE_URL}/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/"
    params = {
        "gameid": cleaned_app_id,
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

    achievements = data.get("achievementpercentages", {}).get("achievements", [])

    if achievements is None:
        return {
            "status_code": 404,
            "error": "No achievement percentages found for the given App ID",
            "achievement_percentages": None,
        }

    simplified_percentages = []
    for achievement in achievements:
        simplified_percentages.append({
            "name": achievement.get("name"),
            "percent": achievement.get("percent"),
        })

    return {
        "status_code": 200,
        "achievement_percentages": simplified_percentages,
    }


def get_achievements_with_rarity(app_id: str):
    achievements_result = get_game_achievements(app_id)
    if achievements_result.get("status_code") != 200:
        return achievements_result

    percentages_result = get_global_achievement_percentages(app_id)
    if percentages_result.get("status_code") != 200:
        return percentages_result

    achievements = achievements_result.get("achievements", [])
    percentages = percentages_result.get("achievement_percentages", [])

    percentage_map = {}
    for achievement in percentages:
        name = achievement.get("name")
        if name:
            percentage_map[name] = achievement.get("percent")

    combined_achievements = []
    for achievement in achievements:
        name = achievement.get("name")
        combined_achievements.append({
            "name": name,
            "display_name": achievement.get("display_name"),
            "description": achievement.get("description"),
            "hidden": achievement.get("hidden"),
            "icon": achievement.get("icon"),
            "global_percentage": percentage_map.get(name),
        })

    return {
        "status_code": 200,
        "game_name": achievements_result.get("game_name"),
        "game_version": achievements_result.get("game_version"),
        "achievements": combined_achievements,
    }

def get_achievements_with_rarity_by_name(game_name: str):
    app_id_result = get_steam_app_id_from_game_name(game_name)
    if app_id_result.get("status_code") != 200:
        return app_id_result

    app_id = app_id_result.get("app_id")
    achievements_result = get_achievements_with_rarity(app_id)

    if achievements_result.get("status_code") != 200:
        return achievements_result

    achievements_result["resolved_app_id"] = app_id
    achievements_result["resolved_game_name"] = app_id_result.get("game_name")
    achievements_result["steam_url"] = app_id_result.get("steam_url")

    return achievements_result
