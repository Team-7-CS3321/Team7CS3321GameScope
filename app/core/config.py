import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
RAWG_API_KEY = os.getenv("RAWG_API_KEY")
