from fastapi import APIRouter
from app.services.steam_service import (
    get_player_summary,
    get_achievements_with_rarity_by_name
)
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/steam", tags=["Steam"])


@router.get("/player/{steam_id}")
def steam_player_summary(steam_id: str):
    result = get_player_summary(steam_id)

    if result["status_code"] != 200:
        return error_response(
            code = "Steam_Web_API_Error",
            message = result.get("error", "Unknown Steam Player Error"),
            status_code = result["status_code"]
        )
    else:
        return success_response(
            data = {
                "player": result["player"]
            }
        )

@router.get("/achievements/{game_name}")
def steam_achievements(game_name: str):
    result = get_achievements_with_rarity_by_name(game_name)

    if result["status_code"] != 200:
        return error_response(
            code="Steam_Achievement_Error",
            message=result.get("error", "Unknown Steam Achievement Error"),
            status_code=result["status_code"]
        )
    else:
        return success_response(
            data={
                "game_name": result.get("resolved_game_name"),
                "app_id": result.get("resolved_app_id"),
                "steam_url": result.get("steam_url"),
                "achievements": result.get("achievements", []),
            }
        )
