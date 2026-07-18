from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.farm import FarmCreate, FarmResponse, FarmUpdate
from app.services import farm_service
from app.utils.response import success_response

router = APIRouter(prefix="/farms", tags=["Farms"])


def _serialize(farm) -> dict:
    return FarmResponse.model_validate(farm).model_dump(mode="json")


@router.get("", summary="Ambil seluruh data farm")
def get_all_farms(db: Session = Depends(get_db)):
    farms = farm_service.get_all_farms(db)
    return success_response(
        data=[_serialize(f) for f in farms],
        message="Farms retrieved successfully",
    )


@router.get("/{farm_id}", summary="Ambil data farm berdasarkan ID")
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = farm_service.get_farm_by_id(db, farm_id)
    return success_response(
        data=_serialize(farm),
        message="Farm retrieved successfully",
    )


@router.post("", status_code=201, summary="Buat farm baru")
def create_farm(farm_data: FarmCreate, db: Session = Depends(get_db)):
    farm = farm_service.create_farm(db, farm_data)
    return success_response(
        data=_serialize(farm),
        message="Farm created successfully",
        status_code=201,
    )


@router.put("/{farm_id}", summary="Update data farm")
def update_farm(farm_id: int, farm_data: FarmUpdate, db: Session = Depends(get_db)):
    farm = farm_service.update_farm(db, farm_id, farm_data)
    return success_response(
        data=_serialize(farm),
        message="Farm updated successfully",
    )


@router.delete("/{farm_id}", summary="Hapus farm")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = farm_service.delete_farm(db, farm_id)
    return success_response(
        data=_serialize(farm),
        message="Farm deleted successfully",
    )
