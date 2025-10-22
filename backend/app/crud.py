"""
CRUD Operations
Database operations for apartment units
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from . import models, schemas


def get_unit(db: Session, unit_id: str) -> Optional[models.Unit]:
    """
    Get a single unit by ID
    """
    return db.query(models.Unit).filter(models.Unit.id == unit_id).first()


def get_units(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    bedrooms: Optional[int] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None,
    city: Optional[str] = None
) -> List[models.Unit]:
    """
    Get units with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        status: Filter by unit status (available, pending, leased)
        bedrooms: Filter by number of bedrooms
        price_min: Minimum price filter
        price_max: Maximum price filter
        city: Filter by city

    Returns:
        List of Unit objects matching filters
    """
    query = db.query(models.Unit)

    # Apply filters
    if status:
        query = query.filter(models.Unit.status == status)

    if bedrooms is not None:
        query = query.filter(models.Unit.bedrooms == bedrooms)

    if price_min is not None:
        query = query.filter(models.Unit.price >= price_min)

    if price_max is not None:
        query = query.filter(models.Unit.price <= price_max)

    if city:
        # JSON field filtering (SQLite-compatible)
        query = query.filter(models.Unit.location.contains(city))

    # Order by lead score descending (highest priority first)
    query = query.order_by(models.Unit.lead_score.desc())

    return query.offset(skip).limit(limit).all()


def get_units_count(
    db: Session,
    status: Optional[str] = None,
    bedrooms: Optional[int] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None
) -> int:
    """
    Get count of units matching filters (for pagination)
    """
    query = db.query(models.Unit)

    if status:
        query = query.filter(models.Unit.status == status)
    if bedrooms is not None:
        query = query.filter(models.Unit.bedrooms == bedrooms)
    if price_min is not None:
        query = query.filter(models.Unit.price >= price_min)
    if price_max is not None:
        query = query.filter(models.Unit.price <= price_max)

    return query.count()


def create_unit(db: Session, unit: schemas.UnitCreate) -> models.Unit:
    """
    Create a new apartment unit
    """
    db_unit = models.Unit(
        property_name=unit.property_name,
        unit_number=unit.unit_number,
        bedrooms=unit.bedrooms,
        bathrooms=unit.bathrooms,
        square_feet=unit.square_feet,
        price=unit.price,
        status=unit.status,
        amenities=unit.amenities,
        location=unit.location.model_dump(),
        images=unit.images,
        description=unit.description,
        date_listed=datetime.utcnow()
    )

    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)

    return db_unit


def update_unit(
    db: Session,
    unit_id: str,
    unit_update: schemas.UnitUpdate
) -> Optional[models.Unit]:
    """
    Update an existing unit
    Key operation for leasing workflow (status changes)
    """
    db_unit = get_unit(db, unit_id)

    if not db_unit:
        return None

    # Update only provided fields
    update_data = unit_update.model_dump(exclude_unset=True)

    # Special handling for location (Pydantic model to dict)
    if "location" in update_data and update_data["location"]:
        update_data["location"] = update_data["location"].model_dump()

    # If status changed to leased, set date_leased
    if "status" in update_data and update_data["status"] == "leased":
        update_data["date_leased"] = datetime.utcnow()

    # Apply updates
    for key, value in update_data.items():
        setattr(db_unit, key, value)

    db_unit.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_unit)

    return db_unit


def delete_unit(db: Session, unit_id: str) -> bool:
    """
    Delete a unit (admin operation)
    """
    db_unit = get_unit(db, unit_id)

    if not db_unit:
        return False

    db.delete(db_unit)
    db.commit()

    return True


def get_leased_units(db: Session) -> List[models.Unit]:
    """
    Get all leased units (for analytics)
    """
    return db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.LEASED
    ).all()


def get_available_units(db: Session) -> List[models.Unit]:
    """
    Get all available units (for analytics)
    """
    return db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).all()


def update_lead_score(db: Session, unit_id: str, new_score: float) -> Optional[models.Unit]:
    """
    Update lead score for a unit
    Called by lead scoring algorithm
    """
    db_unit = get_unit(db, unit_id)

    if not db_unit:
        return None

    db_unit.lead_score = new_score
    db_unit.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_unit)

    return db_unit
