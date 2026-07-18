"""
Farm service module.

Contains the business logic for farm CRUD operations.
Communicates with the database through SQLAlchemy sessions.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmUpdate


def get_all_farms(db: Session) -> list[Farm]:
    """
    Retrieve all farm records from the database.

    Args:
        db: Active database session.

    Returns:
        A list of all Farm objects.
    """
    return db.query(Farm).order_by(Farm.id).all()


def get_farm_by_id(db: Session, farm_id: int) -> Farm:
    """
    Retrieve a single farm by its primary key.

    Args:
        db: Active database session.
        farm_id: The ID of the farm to retrieve.

    Returns:
        The matching Farm object.

    Raises:
        HTTPException: 404 if the farm is not found.
    """
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm


def create_farm(db: Session, farm_data: FarmCreate) -> Farm:
    """
    Create a new farm record in the database.

    Args:
        db: Active database session.
        farm_data: Validated farm creation data.

    Returns:
        The newly created Farm object.
    """
    new_farm = Farm(**farm_data.model_dump())
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)
    return new_farm


def update_farm(db: Session, farm_id: int, farm_data: FarmUpdate) -> Farm:
    """
    Update an existing farm record with partial data.

    Only fields provided in the request body (non-None) will be updated.

    Args:
        db: Active database session.
        farm_id: The ID of the farm to update.
        farm_data: Validated farm update data.

    Returns:
        The updated Farm object.

    Raises:
        HTTPException: 404 if the farm is not found.
    """
    farm = get_farm_by_id(db, farm_id)

    update_fields = farm_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(farm, field, value)

    db.commit()
    db.refresh(farm)
    return farm


def delete_farm(db: Session, farm_id: int) -> Farm:
    """
    Delete a farm record from the database.

    Args:
        db: Active database session.
        farm_id: The ID of the farm to delete.

    Returns:
        The deleted Farm object (for response purposes).

    Raises:
        HTTPException: 404 if the farm is not found.
    """
    farm = get_farm_by_id(db, farm_id)
    db.delete(farm)
    db.commit()
    return farm
