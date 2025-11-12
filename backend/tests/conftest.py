"""
Pytest Configuration and Fixtures
Shared test setup and utilities
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.database import Base, get_db
from app.main import app
from app.models import Unit, UnitStatus


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_leaseflow.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with dependency override
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_unit_data():
    """
    Sample unit data for testing
    """
    return {
        "property_name": "Test Apartments",
        "unit_number": "101",
        "bedrooms": 2,
        "bathrooms": 1.5,
        "square_feet": 950,
        "price": 1200,
        "status": "available",
        "amenities": ["parking", "dishwasher", "air_conditioning"],
        "location": {
            "address": "123 Test St",
            "city": "Louisville",
            "state": "KY",
            "zip": "40202",
            "lat": 38.2527,
            "lng": -85.7585
        },
        "images": ["https://example.com/image1.jpg"],
        "description": "Beautiful 2-bedroom apartment in downtown Louisville"
    }


@pytest.fixture
def sample_unit(db_session, sample_unit_data):
    """
    Create a sample unit in the database
    """
    unit = Unit(
        id="test-unit-001",
        property_name=sample_unit_data["property_name"],
        unit_number=sample_unit_data["unit_number"],
        bedrooms=sample_unit_data["bedrooms"],
        bathrooms=sample_unit_data["bathrooms"],
        square_feet=sample_unit_data["square_feet"],
        price=sample_unit_data["price"],
        status=UnitStatus.AVAILABLE,
        amenities=sample_unit_data["amenities"],
        location=sample_unit_data["location"],
        images=sample_unit_data["images"],
        description=sample_unit_data["description"],
        lead_score=50.0,
        date_listed=datetime.utcnow()
    )
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(unit)
    return unit


@pytest.fixture
def multiple_units(db_session):
    """
    Create multiple units for testing analytics and queries
    """
    units = [
        Unit(
            id=f"test-unit-{i:03d}",
            property_name=f"Property {i}",
            unit_number=f"{100 + i}",
            bedrooms=(i % 3) + 1,
            bathrooms=1.0 + (i % 2) * 0.5,
            square_feet=800 + (i * 50),
            price=1000 + (i * 100),
            status=UnitStatus.AVAILABLE if i % 3 == 0 else (UnitStatus.LEASED if i % 3 == 1 else UnitStatus.PENDING),
            amenities=["parking"] if i % 2 == 0 else ["dishwasher"],
            location={
                "address": f"{i} Test St",
                "city": "Louisville",
                "state": "KY",
                "zip": "40202",
                "lat": 38.2527,
                "lng": -85.7585
            },
            images=[],
            description=f"Test unit number {i}",
            lead_score=50.0 + (i * 5),
            date_listed=datetime.utcnow() - timedelta(days=i),
            date_leased=datetime.utcnow() - timedelta(days=i-5) if i % 3 == 1 else None
        )
        for i in range(10)
    ]
    db_session.add_all(units)
    db_session.commit()
    return units
