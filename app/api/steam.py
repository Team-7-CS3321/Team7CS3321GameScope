from fastapi import APIRouter, Query
from app.services.steam_service import get_achievements_with_rarity
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/steam", tags=["Steam"])


@router.get(
    "/achievements",
    summary="Get Steam achievements with rarity",
    description="Returns Steam achievements and global rarity percentages for a given Steam app ID."
)
def steam_achievements(app_id: str = Query(..., description="Steam app ID, such as 1245620 for Elden Ring")):
    result = get_achievements_with_rarity(app_id)

    if result["status_code"] != 200:
        return error_response(
            code="STEAM_ACHIEVEMENT_ERROR",
            message=result.get("error", "Unknown Steam achievement error"),
            status_code=result["status_code"]
        )

    return success_response(
        data={
            "game_name": result.get("game_name"),
            "game_version": result.get("game_version"),
            "achievements": result.get("achievements", []),
        }
    )
