"""
Lead Scoring Algorithm Tests
Tests for lead_scoring.py functionality
"""

import pytest
from datetime import datetime, timedelta
from app import lead_scoring
from app.models import Unit, UnitStatus


def test_get_market_data(db_session, multiple_units):
    """Test calculating market data from units"""
    market_data = lead_scoring.get_market_data(db_session)

    assert "average_price" in market_data
    assert "average_price_per_sqft" in market_data
    assert "total_units" in market_data
    # Only available units are counted
    available_count = sum(1 for u in multiple_units if u.status.value == "available")
    assert market_data["total_units"] == available_count
    if available_count > 0:
        assert market_data["average_price"] > 0


def test_calculate_lead_score_basic(db_session, sample_unit):
    """Test basic lead score calculation"""
    market_data = lead_scoring.get_market_data(db_session)
    score = lead_scoring.calculate_lead_score(sample_unit, market_data)

    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_calculate_score_breakdown(db_session, sample_unit):
    """Test detailed score breakdown calculation"""
    market_data = lead_scoring.get_market_data(db_session)
    breakdown = lead_scoring.calculate_score_breakdown(sample_unit, market_data)

    assert "total_score" in breakdown
    assert "components" in breakdown
    assert "price_competitiveness" in breakdown["components"]
    assert "listing_freshness" in breakdown["components"]
    assert "desirable_features" in breakdown["components"]
    assert "unit_size_appeal" in breakdown["components"]
    assert "location_desirability" in breakdown["components"]
    assert "explanation" in breakdown


def test_price_competitiveness_below_market(db_session):
    """Test price competitiveness scoring for below-market pricing"""
    # Create market units with average price around $1600
    market_units = [
        Unit(
            id=f"test-market-{i}",
            property_name="Market Unit",
            unit_number=str(i),
            bedrooms=2,
            bathrooms=1.5,
            square_feet=1000,
            price=1500 + (i * 100),
            status=UnitStatus.AVAILABLE,
            amenities=[],
            location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
            images=[],
            description="Market unit",
            date_listed=datetime.utcnow()
        )
        for i in range(3)
    ]
    db_session.add_all(market_units)

    # Now add the cheap unit
    unit = Unit(
        id="test-cheap",
        property_name="Cheap Place",
        unit_number="1",
        bedrooms=2,
        bathrooms=1.5,
        square_feet=1000,
        price=1000,  # Below market average
        status=UnitStatus.AVAILABLE,
        amenities=[],
        location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
        images=[],
        description="Test unit with below-market pricing",
        date_listed=datetime.utcnow()
    )
    db_session.add(unit)
    db_session.commit()

    market_data = lead_scoring.get_market_data(db_session)
    breakdown = lead_scoring.calculate_score_breakdown(unit, market_data)

    # Below market should get positive points
    assert breakdown["components"]["price_competitiveness"] > 0


def test_listing_freshness_new(db_session):
    """Test listing freshness scoring for brand new listing"""
    unit = Unit(
        id="test-new",
        property_name="New Place",
        unit_number="1",
        bedrooms=2,
        bathrooms=1.5,
        square_feet=1000,
        price=1200,
        status=UnitStatus.AVAILABLE,
        amenities=[],
        location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
        images=[],
        description="Brand new listing",
        date_listed=datetime.utcnow()  # Listed today
    )
    db_session.add(unit)
    db_session.commit()

    market_data = lead_scoring.get_market_data(db_session)
    breakdown = lead_scoring.calculate_score_breakdown(unit, market_data)

    # New listing should get maximum freshness points
    assert breakdown["components"]["listing_freshness"] == 15


def test_listing_freshness_stale(db_session):
    """Test listing freshness scoring for old listing"""
    unit = Unit(
        id="test-old",
        property_name="Old Place",
        unit_number="1",
        bedrooms=2,
        bathrooms=1.5,
        square_feet=1000,
        price=1200,
        status=UnitStatus.AVAILABLE,
        amenities=[],
        location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
        images=[],
        description="Old listing",
        date_listed=datetime.utcnow() - timedelta(days=60)  # 60 days old
    )
    db_session.add(unit)
    db_session.commit()

    market_data = lead_scoring.get_market_data(db_session)
    breakdown = lead_scoring.calculate_score_breakdown(unit, market_data)

    # Old listing should get negative freshness points
    assert breakdown["components"]["listing_freshness"] < 0


def test_desirable_features_high_value(db_session):
    """Test desirable features scoring with high-value amenities"""
    unit = Unit(
        id="test-amenities",
        property_name="Premium Place",
        unit_number="1",
        bedrooms=2,
        bathrooms=1.5,
        square_feet=1000,
        price=1200,
        status=UnitStatus.AVAILABLE,
        amenities=["parking", "washer_dryer", "dishwasher", "air_conditioning"],
        location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
        images=[],
        description="Unit with premium amenities",
        date_listed=datetime.utcnow()
    )
    db_session.add(unit)
    db_session.commit()

    market_data = lead_scoring.get_market_data(db_session)
    score = lead_scoring.calculate_lead_score(unit, market_data)

    # High-value amenities should score well
    assert score > 50  # Should be above base score


def test_unit_size_appeal_optimal(db_session):
    """Test unit size appeal for optimal bedroom count"""
    unit = Unit(
        id="test-size",
        property_name="Right Size",
        unit_number="1",
        bedrooms=2,  # Optimal size
        bathrooms=2.0,
        square_feet=1000,
        price=1200,
        status=UnitStatus.AVAILABLE,
        amenities=[],
        location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
        images=[],
        description="Well-sized unit",
        date_listed=datetime.utcnow()
    )
    db_session.add(unit)
    db_session.commit()

    market_data = lead_scoring.get_market_data(db_session)
    score = lead_scoring.calculate_lead_score(unit, market_data)

    # 2-bedroom with 2 bathrooms should score well
    assert score > 50  # Should be above base score


def test_location_desirability_prime_zip(db_session):
    """Test location desirability for prime zip code"""
    unit = Unit(
        id="test-location",
        property_name="Prime Location",
        unit_number="1",
        bedrooms=2,
        bathrooms=1.5,
        square_feet=1000,
        price=1200,
        status=UnitStatus.AVAILABLE,
        amenities=[],
        location={"address": "1 St", "city": "Louisville", "state": "KY", "zip": "40202", "lat": 38.25, "lng": -85.76},
        images=[],
        description="Prime zip code location",
        date_listed=datetime.utcnow()
    )
    db_session.add(unit)
    db_session.commit()

    market_data = lead_scoring.get_market_data(db_session)
    score = lead_scoring.calculate_lead_score(unit, market_data)

    # 40202 is a prime zip code in Louisville, should get location bonus
    assert score > 50  # Should get location bonus points


def test_recalculate_all_scores(db_session, multiple_units):
    """Test batch recalculation of all lead scores"""
    # Set all scores to 0
    for unit in multiple_units:
        unit.lead_score = 0.0
    db_session.commit()

    # Recalculate
    updated_count = lead_scoring.recalculate_all_scores(db_session)

    assert updated_count > 0

    # Verify scores were updated
    db_session.refresh(multiple_units[0])
    assert multiple_units[0].lead_score != 0.0


def test_score_bounds(db_session, sample_unit):
    """Test that scores are always within valid bounds"""
    market_data = lead_scoring.get_market_data(db_session)

    # Test multiple times with different data
    for _ in range(10):
        score = lead_scoring.calculate_lead_score(sample_unit, market_data)
        assert 0 <= score <= 100
