"""
CRUD Operations Tests
Tests for database operations in crud.py
"""

import pytest
from app import crud
from app.models import UnitStatus
from app.schemas import UnitCreate, UnitUpdate


def test_get_unit(db_session, sample_unit):
    """Test retrieving a single unit by ID"""
    unit = crud.get_unit(db_session, sample_unit.id)
    assert unit is not None
    assert unit.id == sample_unit.id
    assert unit.property_name == sample_unit.property_name


def test_get_unit_not_found(db_session):
    """Test retrieving non-existent unit returns None"""
    unit = crud.get_unit(db_session, "non-existent-id")
    assert unit is None


def test_get_units(db_session, multiple_units):
    """Test retrieving list of units with pagination"""
    units = crud.get_units(db_session, skip=0, limit=5)
    assert len(units) == 5
    assert all(unit.id for unit in units)


def test_get_units_with_status_filter(db_session, multiple_units):
    """Test filtering units by status"""
    available_units = crud.get_units(db_session, status="available")
    assert all(unit.status == UnitStatus.AVAILABLE for unit in available_units)
    assert len(available_units) > 0


def test_get_units_with_bedroom_filter(db_session, multiple_units):
    """Test filtering units by number of bedrooms"""
    units = crud.get_units(db_session, bedrooms=2)
    assert all(unit.bedrooms == 2 for unit in units)


def test_get_units_with_price_range(db_session, multiple_units):
    """Test filtering units by price range"""
    units = crud.get_units(db_session, price_min=1200, price_max=1500)
    assert all(1200 <= unit.price <= 1500 for unit in units)


def test_get_units_with_city_filter(db_session, multiple_units):
    """Test filtering units by city"""
    units = crud.get_units(db_session, city="Louisville")
    assert all(unit.location["city"] == "Louisville" for unit in units)
    assert len(units) == len(multiple_units)


def test_get_units_count(db_session, multiple_units):
    """Test counting total units"""
    total = crud.get_units_count(db_session)
    assert total == len(multiple_units)


def test_create_unit(db_session, sample_unit_data):
    """Test creating a new unit"""
    unit_create = UnitCreate(**sample_unit_data)
    unit = crud.create_unit(db_session, unit_create)

    assert unit.id is not None
    assert unit.property_name == sample_unit_data["property_name"]
    assert unit.unit_number == sample_unit_data["unit_number"]
    assert unit.bedrooms == sample_unit_data["bedrooms"]
    assert unit.price == sample_unit_data["price"]
    assert unit.status == UnitStatus.AVAILABLE


def test_update_unit(db_session, sample_unit):
    """Test updating an existing unit"""
    update_data = UnitUpdate(price=1500, status=UnitStatus.PENDING)
    updated_unit = crud.update_unit(db_session, sample_unit.id, update_data)

    assert updated_unit.id == sample_unit.id
    assert updated_unit.price == 1500
    assert updated_unit.status == UnitStatus.PENDING


def test_update_unit_not_found(db_session):
    """Test updating non-existent unit returns None"""
    update_data = UnitUpdate(price=1500)
    result = crud.update_unit(db_session, "non-existent-id", update_data)
    assert result is None


def test_update_unit_status_to_leased(db_session, sample_unit):
    """Test updating unit status to leased sets date_leased"""
    update_data = UnitUpdate(status=UnitStatus.LEASED)
    updated_unit = crud.update_unit(db_session, sample_unit.id, update_data)

    assert updated_unit.status == UnitStatus.LEASED
    assert updated_unit.date_leased is not None


def test_delete_unit(db_session, sample_unit):
    """Test deleting a unit"""
    result = crud.delete_unit(db_session, sample_unit.id)
    assert result is True

    # Verify unit is deleted
    unit = crud.get_unit(db_session, sample_unit.id)
    assert unit is None


def test_delete_unit_not_found(db_session):
    """Test deleting non-existent unit returns False"""
    result = crud.delete_unit(db_session, "non-existent-id")
    assert result is False


def test_update_lead_score(db_session, sample_unit):
    """Test updating a unit's lead score"""
    new_score = 85.5
    crud.update_lead_score(db_session, sample_unit.id, new_score)

    db_session.refresh(sample_unit)
    assert sample_unit.lead_score == new_score


def test_pagination(db_session, multiple_units):
    """Test pagination works correctly"""
    page1 = crud.get_units(db_session, skip=0, limit=3)
    page2 = crud.get_units(db_session, skip=3, limit=3)

    assert len(page1) == 3
    assert len(page2) == 3
    assert page1[0].id != page2[0].id
