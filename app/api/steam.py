from fastapi import APIRouter
from app.services.steam_service import get_player_summary
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/steam", tags=["Steam"])


@router.get("/player/{steam_id}")
def steam_player_summary(steam_id: str):
    result = get_player_summary(steam_id)

    if result["status_code"] != 200:
        return error_response(
            code = "Steam_Web_API_Error",
            message = result.get("error", "Unknown Steam Error"),
            status_code = result["status_code"]
        )
    else:
        return success_response(
            data = {
                "player": result["player"]
            }
        )
