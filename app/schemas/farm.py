"""Pydantic schemas untuk validasi request dan serialisasi response Farm."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class FarmCreate(BaseModel):
    """Schema untuk membuat farm baru."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nama farm",
        examples=["Green Valley Farm"],
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Lokasi geografis farm",
        examples=["Central Java, Indonesia"],
    )
    size: float = Field(
        ...,
        gt=0,
        description="Ukuran farm dalam hektar",
        examples=[25.5],
    )
    crop_type: Optional[str] = Field(
        None,
        max_length=255,
        description="Jenis tanaman yang dibudidayakan",
        examples=["Rice"],
    )


class FarmUpdate(BaseModel):
    """Schema untuk update farm. Semua field opsional (partial update)."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Nama farm",
        examples=["Green Valley Farm"],
    )
    location: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Lokasi geografis farm",
        examples=["Central Java, Indonesia"],
    )
    size: Optional[float] = Field(
        None,
        gt=0,
        description="Ukuran farm dalam hektar",
        examples=[30.0],
    )
    crop_type: Optional[str] = Field(
        None,
        max_length=255,
        description="Jenis tanaman yang dibudidayakan",
        examples=["Corn"],
    )


class FarmResponse(BaseModel):
    """Schema response untuk satu record farm."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    size: float
    crop_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
