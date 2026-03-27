# Utils

This directory contains **utility functions** used across the application to avoid code duplication and enforce consistency.

Utilities are small, reusable helpers that support core functionality but are not tied to a specific feature or service.

---

## Purpose

The `utils` directory is used to:

* Centralize reusable helper logic
* Reduce duplication across routes and services
* Enforce consistent patterns (especially API responses)
* Keep route handlers clean and readable

---

## Files

### `response.py`

Provides helper functions for generating **standardized API responses**.

All routes should use these helpers instead of manually constructing response dictionaries.

---

## Response Helpers

### `success_response`

Returns a standardized success response.

```python
success_response(data=None, status_code=200)
```

#### Example

```python
return success_response(data={"name": "Elden Ring"})
```

#### Output

```json
{
  "status": "success",
  "data": {...},
  "error": null
}
```

---

### `error_response`

Returns a standardized error response.

```python
error_response(message: str, code: str = "UNKNOWN_ERROR", status_code=400)
```

#### Example

```python
return error_response(
    message="Game not found",
    code="GAME_NOT_FOUND",
    status_code=404
)
```

#### Output

```json
{
  "status": "error",
  "data": null,
  "error": {
    "code": "GAME_NOT_FOUND",
    "message": "Game not found"
  }
}
```

---

## Design Notes

* These helpers ensure all endpoints return responses in a **consistent format**
* Routes should always use these functions instead of returning raw dictionaries
* This approach simplifies frontend integration and debugging
* Keeps business logic separate from response formatting

---

## Guidelines

* Do not construct response dictionaries manually in routes
* Do not return raw service outputs directly to the client
* Always wrap responses using `success_response` or `error_response`

---

## Example Usage in a Route

```python
from app.utils.response import success_response, error_response

@router.get("/example")
def example():
    try:
        data = {"message": "Hello World"}
        return success_response(data=data)
    except Exception:
        return error_response(
            message="Something went wrong",
            code="INTERNAL_SERVER_ERROR",
            status_code=500
        )
```
