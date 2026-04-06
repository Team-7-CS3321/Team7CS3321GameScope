from fastapi import APIRouter, Query
from app.services.rawg_service import search_for_steam_game_by_name
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/rawg", tags=["RAWG"])


@router.get(
    "/search",
    summary="Search for a Steam game using RAWG",
    description="Finds the first RAWG result that matches the query and is available on Steam."
)
def rawg_search(query: str = Query(..., description="Game title to search for")):
    result = search_for_steam_game_by_name(query)

    if result["status_code"] != 200:
        return error_response(
            code="RAWG_API_ERROR",
            message=result.get("error", "Unknown RAWG error"),
            status_code=result["status_code"]
        )

    return success_response(
        data={
            "game": result.get("game")
        }
    )
