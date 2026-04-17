from fastapi import FastAPI
from team7cs3321gamescope.api import steam, rawg, combined
from team7cs3321gamescope.core.config import STEAM_API_KEY, RAWG_API_KEY

app = FastAPI(title="Team 7 GameScope API")

app.include_router(steam.router)
app.include_router(rawg.router)
app.include_router(combined.router)


@app.get("/")
def root():
    return {
        "message": "GameScope backend is running",
        "steam_key_loaded": STEAM_API_KEY is not None,
        "rawg_key_loaded": RAWG_API_KEY is not None,
    }
