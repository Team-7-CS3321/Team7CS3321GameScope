from fastapi import APIRouter
from app.services.rawg_service import search_games
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/rawg", tags=["RAWG"])


@router.get("/search")
def rawg_search(query: str):
    result = search_games(query)

    if result["status_code"] != 200:
        return error_response(
            code = "RAWG_API_ERROR",
            message = result.get("error", "Unknown RAWG Error"),
            status_code = result["status_code"]
        )
    else:
        return success_response(
            data = {
                "count": result["count"],
                "results": result["results"]
                }
        )
