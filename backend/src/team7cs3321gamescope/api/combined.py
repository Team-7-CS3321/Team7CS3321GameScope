from fastapi import APIRouter, Query
from team7cs3321gamescope.services.combined_service import get_full_report
from team7cs3321gamescope.utils.response import success_response, error_response

router = APIRouter(prefix="/report", tags=["Report"])


@router.get(
    "/",
    summary="Get full game report",
    description="Returns a full Steam-focused game report using RAWG metadata and Steam achievement rarity data."
)
def game_report(game_name: str = Query(..., description="Steam game title to search for")):
    result = get_full_report(game_name)

    if result.get("status_code") != 200:
        return error_response(
            code="GAME_REPORT_ERROR",
            message=result.get("error", "Unknown game report error"),
            status_code=result["status_code"],
        )

    return success_response(
        data={
            "game": result.get("game")
        }
    )
