import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from team7cs3321gamescope.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def mock_api_keys():
    with patch("team7cs3321gamescope.services.steam_service.STEAM_API_KEY", "fake_steam_key"), \
         patch("team7cs3321gamescope.services.rawg_service.RAWG_API_KEY", "fake_rawg_key"), \
         patch("team7cs3321gamescope.core.config.STEAM_API_KEY", "fake_steam_key"), \
         patch("team7cs3321gamescope.core.config.RAWG_API_KEY", "fake_rawg_key"):
        yield
