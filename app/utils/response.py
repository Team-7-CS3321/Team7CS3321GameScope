from fastapi.responses import JSONResponse


def success_response(data=None, status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "data": data,
            "error": None
        }
    )


def error_response(code: str, message: str, status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "data": None,
            "error": {
                "code": code,
                "message": message
            }
        }
    )
