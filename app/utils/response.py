"""
Response utility module.

Provides helper functions to create consistent API responses
throughout the application.
"""

from typing import Any

from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Request completed successfully",
    status_code: int = 200,
) -> JSONResponse:
    """
    Create a standardized success response.

    Args:
        data: The response payload (serialized before passing).
        message: A human-readable success message.
        status_code: HTTP status code (default 200).

    Returns:
        A JSONResponse with the consistent envelope.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
) -> JSONResponse:
    """
    Create a standardized error response.

    Args:
        message: A human-readable error message.
        status_code: HTTP status code (default 400).

    Returns:
        A JSONResponse with the consistent envelope.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
        },
    )
