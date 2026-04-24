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
- React
- Vite

## Running the Project

1. Clone the repository
2. Use "cd" to move to "~/Team73321GameScope/backend
3. Install dependencies:
   ```bash
   uv sync --all-groups
4. Run the local server:
    ```bash

   .venv\Scripts\activatedoppler run -- uv run uvicorn team7cs3321gamescope.main:app --reload --app-dir src
5. In a new Terminal
     ```bash

     
   cd Team7CS3321GameScope/frontend
     
   npm run dev
7. While server is running:
   Swagger docs available at: http://127.0.0.1:8000/docs
   
   Website available at: http://localhost:5173

## Notes
1. .env is not committed via .gitignore
2. uv.lock is committed to ensure dependencies are up to date
