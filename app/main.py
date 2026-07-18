from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.exceptions import register_exception_handlers
from app.routes.farm_routes import router as farm_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Farm Management REST API",
    description=(
        "Backend service untuk mengelola data farm melalui RESTful API. "
        "Dikembangkan sebagai bagian dari Coding Test PT AIGRA EON INDONESIA."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(farm_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "success": True,
        "message": "Farm Management REST API is running",
        "data": None,
    }
