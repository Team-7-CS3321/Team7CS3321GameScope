# Services

This folder contains service-layer logic.

Service files are responsible for:
- calling external APIs
- transforming response data
- handling service-level errors

## Files

- `steam_service.py`  
  Steam Web API integration

- `rawg_service.py`  
  RAWG API integration

## Notes

- This folder should not contain FastAPI route definitions, these should be placed in app/api
- Keep API request logic here, not in `api/`
