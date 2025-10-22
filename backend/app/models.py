"""
SQLAlchemy ORM Models
Database models for apartment units and related entities
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base
import uuid


class UnitStatus(str, enum.Enum):
    """Enum for unit availability status"""
    AVAILABLE = "available"
    PENDING = "pending"
    LEASED = "leased"


class Unit(Base):
    """
    Apartment unit model
    Represents a single rentable unit with all attributes
    """
    __tablename__ = "units"

    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Property Information
    property_name = Column(String, nullable=False, index=True)
    unit_number = Column(String, nullable=False)

    # Unit Specifications
    bedrooms = Column(Integer, nullable=False, index=True)
    bathrooms = Column(Float, nullable=False)
    square_feet = Column(Integer, nullable=False)

    # Pricing & Status
    price = Column(Integer, nullable=False, index=True)
    status = Column(SQLEnum(UnitStatus), nullable=False, default=UnitStatus.AVAILABLE, index=True)

    # Features & Amenities (stored as JSON array)
    amenities = Column(JSON, nullable=False, default=list)

    # Location (stored as JSON object)
    location = Column(JSON, nullable=False)

    # Images (stored as JSON array of URLs)
    images = Column(JSON, nullable=False, default=list)

    # Description
    description = Column(String, nullable=False)

    # Lead Prioritization
    lead_score = Column(Float, default=50.0, index=True)

    # Timestamps
    date_listed = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_leased = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Unit {self.property_name} - {self.unit_number} ({self.status})>"

    def to_dict(self):
        """
        Convert model to dictionary for JSON serialization
        """
        return {
            "id": self.id,
            "property_name": self.property_name,
            "unit_number": self.unit_number,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "square_feet": self.square_feet,
            "price": self.price,
            "status": self.status.value,
            "amenities": self.amenities,
            "location": self.location,
            "images": self.images,
            "description": self.description,
            "lead_score": self.lead_score,
            "date_listed": self.date_listed.isoformat() if self.date_listed else None,
            "date_leased": self.date_leased.isoformat() if self.date_leased else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
