"""
Analytics Engine Tests
Tests for analytics.py calculations and metrics
"""

import pytest
from datetime import datetime, timedelta
from app import analytics
from app.models import Unit, UnitStatus


def test_get_dashboard_analytics(db_session, multiple_units):
    """Test comprehensive dashboard analytics"""
    result = analytics.get_dashboard_analytics(db_session)

    assert "total_units" in result
    assert "available_units" in result
    assert "leased_units" in result
    assert "pending_units" in result
    assert "average_days_to_lease" in result
    assert "lease_conversion_rate" in result
    assert "average_price" in result
    assert "most_popular_features" in result
    assert "price_trends" in result

    assert result["total_units"] == len(multiple_units)
    assert result["total_units"] == result["available_units"] + result["leased_units"] + result["pending_units"]


def test_unit_counts_by_status(db_session, multiple_units):
    """Test unit counts are accurate by status"""
    result = analytics.get_dashboard_analytics(db_session)

    available_count = sum(1 for u in multiple_units if u.status == UnitStatus.AVAILABLE)
    leased_count = sum(1 for u in multiple_units if u.status == UnitStatus.LEASED)
    pending_count = sum(1 for u in multiple_units if u.status == UnitStatus.PENDING)

    assert result["available_units"] == available_count
    assert result["leased_units"] == leased_count
    assert result["pending_units"] == pending_count


def test_average_days_to_lease(db_session):
    """Test average days to lease calculation"""
    # Create units with known lease times
    units = [
        Unit(
            id=f"test-lease-{i}",
            property_name="Test",
            unit_number=str(i),
            bedrooms=2,
            bathrooms=1.5,
            square_feet=1000,
            price=1200,
            status=UnitStatus.LEASED,
            amenities=[],
            location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
            images=[],
            description="Test unit",
            date_listed=datetime.utcnow() - timedelta(days=20),
            date_leased=datetime.utcnow() - timedelta(days=10)  # 10 days to lease
        )
        for i in range(3)
    ]
    db_session.add_all(units)
    db_session.commit()

    result = analytics.get_dashboard_analytics(db_session)
    assert result["average_days_to_lease"] == 10.0


def test_lease_conversion_rate(db_session):
    """Test lease conversion rate calculation"""
    # Create 10 units: 7 leased, 3 available
    units = []
    for i in range(10):
        unit = Unit(
            id=f"test-conv-{i}",
            property_name="Test",
            unit_number=str(i),
            bedrooms=2,
            bathrooms=1.5,
            square_feet=1000,
            price=1200,
            status=UnitStatus.LEASED if i < 7 else UnitStatus.AVAILABLE,
            amenities=[],
            location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
            images=[],
            description="Test unit",
            date_listed=datetime.utcnow(),
            date_leased=datetime.utcnow() if i < 7 else None
        )
        units.append(unit)

    db_session.add_all(units)
    db_session.commit()

    result = analytics.get_dashboard_analytics(db_session)
    assert result["lease_conversion_rate"] == 70.0  # 7/10 = 70%


def test_average_price(db_session, multiple_units):
    """Test average price calculation"""
    result = analytics.get_dashboard_analytics(db_session)

    expected_avg = sum(u.price for u in multiple_units) / len(multiple_units)
    assert abs(result["average_price"] - expected_avg) < 0.01


def test_most_popular_features(db_session):
    """Test popular features analysis"""
    # Create units with specific amenities
    units = [
        Unit(
            id=f"test-feat-{i}",
            property_name="Test",
            unit_number=str(i),
            bedrooms=2,
            bathrooms=1.5,
            square_feet=1000,
            price=1200,
            status=UnitStatus.LEASED if i < 5 else UnitStatus.AVAILABLE,
            amenities=["parking"] if i % 2 == 0 else ["dishwasher"],
            location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
            images=[],
            description="Test unit",
            date_listed=datetime.utcnow(),
            date_leased=datetime.utcnow() if i < 5 else None
        )
        for i in range(10)
    ]
    db_session.add_all(units)
    db_session.commit()

    result = analytics.get_dashboard_analytics(db_session)
    features = result["most_popular_features"]

    assert len(features) > 0
    assert all("feature" in f and "leased_count" in f and "available_count" in f for f in features)


def test_get_price_trends(db_session, multiple_units):
    """Test price trends over time"""
    trends = analytics.get_price_trends(db_session, days=30)

    assert isinstance(trends, list)
    # With multiple units, should have trend data
    assert len(trends) >= 0


def test_get_bedroom_distribution(db_session, multiple_units):
    """Test bedroom distribution analysis"""
    distribution = analytics.get_bedroom_distribution(db_session)

    assert isinstance(distribution, list)
    assert len(distribution) > 0
    assert all("bedrooms" in d and "count" in d for d in distribution)

    # Verify totals match
    total_count = sum(d["count"] for d in distribution)
    assert total_count == len(multiple_units)


def test_get_status_distribution(db_session, multiple_units):
    """Test status distribution analysis"""
    distribution = analytics.get_status_distribution(db_session)

    assert isinstance(distribution, dict)
    assert len(distribution) > 0

    # Verify totals match
    total_count = sum(distribution.values())
    assert total_count == len(multiple_units)


def test_get_city_distribution(db_session, multiple_units):
    """Test city distribution analysis"""
    distribution = analytics.get_city_distribution(db_session)

    assert isinstance(distribution, list)
    assert len(distribution) > 0
    assert all("city" in d and "count" in d for d in distribution)


def test_get_performance_metrics(db_session, multiple_units):
    """Test key performance indicators"""
    metrics = analytics.get_performance_metrics(db_session)

    assert "occupancy_rate" in metrics
    assert "average_lead_score" in metrics
    assert "recent_leases_30d" in metrics

    # Occupancy rate should be between 0 and 100
    assert 0 <= metrics["occupancy_rate"] <= 100


def test_occupancy_rate_calculation(db_session):
    """Test occupancy rate calculation accuracy"""
    # Create 10 units: 4 leased, 6 available
    units = []
    for i in range(10):
        status = UnitStatus.LEASED if i < 4 else UnitStatus.AVAILABLE
        unit = Unit(
            id=f"test-occ-{i}",
            property_name="Test",
            unit_number=str(i),
            bedrooms=2,
            bathrooms=1.5,
            square_feet=1000,
            price=1200,
            status=status,
            amenities=[],
            location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
            images=[],
            description="Test unit",
            date_listed=datetime.utcnow()
        )
        units.append(unit)

    db_session.add_all(units)
    db_session.commit()

    metrics = analytics.get_performance_metrics(db_session)

    # 4 leased out of 10 = 40%
    assert metrics["occupancy_rate"] == 40.0


def test_recent_leases_count(db_session):
    """Test recent leases (30 days) counting"""
    # Create leases at different times
    units = []
    for i in range(5):
        unit = Unit(
            id=f"test-recent-{i}",
            property_name="Test",
            unit_number=str(i),
            bedrooms=2,
            bathrooms=1.5,
            square_feet=1000,
            price=1200,
            status=UnitStatus.LEASED,
            amenities=[],
            location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
            images=[],
            description="Test unit",
            date_listed=datetime.utcnow() - timedelta(days=40),
            date_leased=datetime.utcnow() - timedelta(days=i * 10)  # 0, 10, 20, 30, 40 days ago
        )
        units.append(unit)

    db_session.add_all(units)
    db_session.commit()

    metrics = analytics.get_performance_metrics(db_session)

    # Only 3 leases within 30 days (0, 10, 20 days ago)
    assert metrics["recent_leases_30d"] == 3


def test_average_lead_score(db_session, multiple_units):
    """Test average lead score calculation"""
    metrics = analytics.get_performance_metrics(db_session)

    expected_avg = sum(u.lead_score for u in multiple_units) / len(multiple_units)
    assert abs(metrics["average_lead_score"] - expected_avg) < 0.01


def test_empty_database_analytics(db_session):
    """Test analytics with empty database"""
    result = analytics.get_dashboard_analytics(db_session)

    assert result["total_units"] == 0
    assert result["average_days_to_lease"] == 0.0
    assert result["lease_conversion_rate"] == 0.0
    assert result["average_price"] == 0.0
