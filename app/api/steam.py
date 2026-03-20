from fastapi import APIRouter
from app.services.steam_service import get_player_summary

router = APIRouter(prefix="/steam", tags=["Steam"])


@router.get("/player/{steam_id}")
def steam_player_summary(steam_id: str):
    return get_player_summary(steam_id)
