"""
Farm Pydantic schemas.

Defines request and response schemas used for:
- Request validation
- Response serialization
- Data validation
"""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class FarmCreate(BaseModel):
    """Schema for creating a new farm."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the farm",
        examples=["Green Valley Farm"],
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Geographic location of the farm",
        examples=["Central Java, Indonesia"],
    )
    size: float = Field(
        ...,
        gt=0,
        description="Size of the farm in hectares",
        examples=[25.5],
    )
    crop_type: Optional[str] = Field(
        None,
        max_length=255,
        description="Type of crop grown on the farm",
        examples=["Rice"],
    )


class FarmUpdate(BaseModel):
    """Schema for updating an existing farm. All fields are optional."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Name of the farm",
        examples=["Green Valley Farm"],
    )
    location: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Geographic location of the farm",
        examples=["Central Java, Indonesia"],
    )
    size: Optional[float] = Field(
        None,
        gt=0,
        description="Size of the farm in hectares",
        examples=[30.0],
    )
    crop_type: Optional[str] = Field(
        None,
        max_length=255,
        description="Type of crop grown on the farm",
        examples=["Corn"],
    )


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class FarmResponse(BaseModel):
    """Schema for serializing a single farm record in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    size: float
    crop_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ApiResponse(BaseModel):
    """
    Standard API response envelope.

    All endpoints return this structure to ensure consistency.
    """

    success: bool
    message: str
    data: Any = None
