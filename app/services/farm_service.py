from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmUpdate


def get_all_farms(db: Session) -> list[Farm]:
    return db.query(Farm).order_by(Farm.id).all()


def get_farm_by_id(db: Session, farm_id: int) -> Farm:
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm


def create_farm(db: Session, farm_data: FarmCreate) -> Farm:
    new_farm = Farm(**farm_data.model_dump())
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)
    return new_farm


def update_farm(db: Session, farm_id: int, farm_data: FarmUpdate) -> Farm:
    farm = get_farm_by_id(db, farm_id)

    for field, value in farm_data.model_dump(exclude_unset=True).items():
        setattr(farm, field, value)

    db.commit()
    db.refresh(farm)
    return farm


def delete_farm(db: Session, farm_id: int) -> Farm:
    farm = get_farm_by_id(db, farm_id)
    db.delete(farm)
    db.commit()
    return farm
