"""
Farm routes module.

Defines all API endpoints for farm CRUD operations.
Routes are lightweight — business logic lives in the service layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.farm import FarmCreate, FarmResponse, FarmUpdate
from app.services import farm_service
from app.utils.response import success_response

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.get(
    "",
    summary="Retrieve all farms",
    description="Returns a list of all farm records in the database.",
)
def get_all_farms(db: Session = Depends(get_db)):
    """Retrieve all farms."""
    farms = farm_service.get_all_farms(db)
    farms_data = [FarmResponse.model_validate(farm).model_dump(mode="json") for farm in farms]
    return success_response(
        data=farms_data,
        message="Farms retrieved successfully",
    )


@router.get(
    "/{farm_id}",
    summary="Retrieve a farm by ID",
    description="Returns a single farm record matching the provided ID.",
)
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    """Retrieve a farm by its ID."""
    farm = farm_service.get_farm_by_id(db, farm_id)
    farm_data = FarmResponse.model_validate(farm).model_dump(mode="json")
    return success_response(
        data=farm_data,
        message="Farm retrieved successfully",
    )


@router.post(
    "",
    status_code=201,
    summary="Create a new farm",
    description="Creates a new farm record with the provided data.",
)
def create_farm(farm_data: FarmCreate, db: Session = Depends(get_db)):
    """Create a new farm."""
    farm = farm_service.create_farm(db, farm_data)
    farm_response = FarmResponse.model_validate(farm).model_dump(mode="json")
    return success_response(
        data=farm_response,
        message="Farm created successfully",
        status_code=201,
    )


@router.put(
    "/{farm_id}",
    summary="Update an existing farm",
    description="Updates the farm record matching the provided ID with the given data. Only provided fields will be updated.",
)
def update_farm(farm_id: int, farm_data: FarmUpdate, db: Session = Depends(get_db)):
    """Update an existing farm."""
    farm = farm_service.update_farm(db, farm_id, farm_data)
    farm_response = FarmResponse.model_validate(farm).model_dump(mode="json")
    return success_response(
        data=farm_response,
        message="Farm updated successfully",
    )


@router.delete(
    "/{farm_id}",
    summary="Delete a farm",
    description="Deletes the farm record matching the provided ID.",
)
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    """Delete a farm."""
    farm = farm_service.delete_farm(db, farm_id)
    farm_response = FarmResponse.model_validate(farm).model_dump(mode="json")
    return success_response(
        data=farm_response,
        message="Farm deleted successfully",
    )
