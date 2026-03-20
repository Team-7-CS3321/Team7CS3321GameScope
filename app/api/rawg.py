from fastapi import APIRouter
from app.services.rawg_service import search_games

router = APIRouter(prefix="/rawg", tags=["RAWG"])


@router.get("/search")
def rawg_search(query: str):
    return search_games(query)
