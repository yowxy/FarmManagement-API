"""
Farm Management REST API — Application Entry Point.

Creates the FastAPI application, registers routes and exception handlers,
and initializes the database tables on startup.
"""

from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.exceptions import register_exception_handlers
from app.routes.farm_routes import router as farm_router

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Farm Management REST API",
    description=(
        "A backend application for managing farm data through RESTful API services. "
        "Developed as part of the PT AIGRA EON INDONESIA Fullstack Developer "
        "(Backend Focus) Coding Test."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# Register global exception handlers
# ---------------------------------------------------------------------------

register_exception_handlers(app)

# ---------------------------------------------------------------------------
# Register API routes
# ---------------------------------------------------------------------------

app.include_router(farm_router)

# ---------------------------------------------------------------------------
# Create database tables on startup
# ---------------------------------------------------------------------------


@app.on_event("startup")
def on_startup():
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------------------------


@app.get("/", tags=["Root"], summary="Health check")
def root():
    """Root endpoint — confirms the API is running."""
    return {
        "success": True,
        "message": "Farm Management REST API is running",
        "data": None,
    }
