"""
Farm SQLAlchemy model.

Defines the Farm table schema that maps to the 'farms' table
in the PostgreSQL database.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base


class Farm(Base):
    """
    Represents a farm entity in the database.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: Name of the farm (required).
        location: Geographic location of the farm (required).
        size: Size of the farm in hectares (required).
        crop_type: Type of crop grown on the farm (optional).
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    size = Column(Float, nullable=False)
    crop_type = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
