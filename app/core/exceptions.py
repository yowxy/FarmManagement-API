"""
Global exception handlers module.

Registers exception handlers on the FastAPI application to ensure
all errors return a consistent response format.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers on the FastAPI application.

    Handles:
        - RequestValidationError (422)
        - HTTPException (variable status code)
        - Generic Exception (500)
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors with a consistent response format."""
        errors = exc.errors()
        error_messages = []
        for error in errors:
            field = " -> ".join(str(loc) for loc in error.get("loc", []))
            message = error.get("msg", "Invalid value")
            error_messages.append(f"{field}: {message}")

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "data": error_messages,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """Handle HTTP exceptions with a consistent response format."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "data": None,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions with a 500 response."""
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
                "data": None,
            },
        )
