# Team7CS3321GameScope
# Team 7 - GameScope

GameScope is a backend-focused project that combines data from the Steam Web API and RAWG API to provide game search, player information, and future game intelligence features.

## Current Progress

- FastAPI backend initialized
- Steam API integration working
- RAWG API integration working
- Environment configuration set up with `.env`

## Tech Stack

- Python
- FastAPI
- uv
- Steam Web API
- RAWG API

## Running the Project

1. Clone the repository
2. Use "cd" to move to "~/Team73321GameScope/backend
3. Create a `.env` file using `.env.example`
4. Install dependencies:
   ```bash
   uv sync --all-groups
5. Run the local server:
    ```bash
   uv run uvicorn app.main:app --reload
6. While server is running:
   Swagger docs available at: http://127.0.0.1:8000/docs

## Notes
1. .env is not committed via .gitignore
2. uv.lock is committed to ensure dependencies are up to date
