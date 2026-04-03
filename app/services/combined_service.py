from app.services.rawg_service import search_for_steam_game_by_name
from app.services.steam_service import get_achievements_with_rarity


def get_full_report(game_name: str):
    # RAWG lookup
    rawg_result = search_for_steam_game_by_name(game_name)
    if rawg_result.get("status_code") != 200:
        return rawg_result

    game_data = rawg_result.get("game", {})
    app_id = game_data.get("steam_app_id")

    if not app_id:
        return {
            "status_code": 404,
            "error": "Steam app ID not found for this game",
        }

    # Steam achievements
    achievements_result = get_achievements_with_rarity(app_id)
    if achievements_result.get("status_code") != 200:
        return achievements_result

    achievements = achievements_result.get("achievements", [])

    # Difficulty calculation
    difficulty_score = calculate_difficulty_score(achievements)

    # Final response
    return {
        "status_code": 200,
        "game": {
            "name": game_data.get("name"),
            "release_date": game_data.get("release_date"),
            "genres": game_data.get("genres"),
            "tags": game_data.get("tags"),
            "rating": game_data.get("rating"),
            "description": game_data.get("description"),
            "publishers": game_data.get("publishers"),

            "steam_app_id": app_id,
            "steam_url": game_data.get("steam_url"),

            "achievement_count": len(achievements),
            "difficulty_score": difficulty_score,
            "achievements": achievements,
        },
    }


def calculate_difficulty_score(achievements):
    if not achievements:
        return 0

    total = 0
    count = 0

    for achievement in achievements:
        percent = achievement.get("global_percentage")

        if percent is None:
            continue

        try:
            percent = float(percent)
        except (TypeError, ValueError):
            continue

        total += (100 - percent)
        count += 1
    return round(total / count, 2) if count else 0

