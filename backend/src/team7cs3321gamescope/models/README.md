# Models

This directory contains all **Pydantic models** used by the backend.
Models define the structure of data used throughout the application, including API responses and (optionally) request validation.

---

## Purpose

Models are used to:

* Enforce a consistent data structure across the application
* Validate incoming and outgoing data
* Provide a clear contract between the backend and frontend
* Improve readability and maintainability of the codebase

---

## Files

### `response_models.py`

Defines the **standardized API response format** used across all endpoints.

#### Structure

All API responses follow this format:

### Success Response

```json
{
  "status": "success",
  "data": {...},
  "error": null
}
```

### Error Response

```json
{
  "status": "error",
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

#### Models

* **ApiResponse**

  * Represents the overall API response structure
  * Fields:

    * `status`: `"success"` or `"error"`
    * `data`: The returned payload (if successful)
    * `error`: Error details (if a failure occurs)

* **ErrorDetail**

  * Represents error information
  * Fields:

    * `code`: Machine-readable error identifier
    * `message`: Human-readable error message

---

## Design Notes

* The response format is centralized to ensure **consistency across all routes**
* Routes should use helper functions (`success_response`, `error_response`) instead of manually constructing responses
* Services should **not** return this format directly — they return raw data that routes convert into this structure

---

## Usage Example

```python
from app.utils.response import success_response, error_response

# Success
return success_response(data={"name": "Elden Ring"})

# Error
return error_response(
    message="Game not found",
    code="GAME_NOT_FOUND",
    status_code=404
)
```









