"""
Lead Scoring Algorithm
Automated lead prioritization for apartment units
Rule-based scoring system demonstrating AI/automation logic
"""

from datetime import datetime, timedelta
from typing import Dict, List
from . import models
from sqlalchemy.orm import Session


def calculate_lead_score(unit: models.Unit, market_data: Dict) -> float:
    """
    Calculate lead score for an apartment unit (0-100)

    This rule-based algorithm mimics ML-based lead prioritization
    In production, this would be a trained model using historical leasing data

    Scoring Factors:
    1. Price Competitiveness (vs market average)
    2. Listing Freshness (urgency factor)
    3. Desirable Features (amenity scoring)
    4. Unit Size Appeal
    5. Location Desirability

    Args:
        unit: Unit object to score
        market_data: Dictionary containing market statistics

    Returns:
        Score from 0-100 (higher = more likely to lease quickly)
    """
    score = 50.0  # Base score

    # 1. Price Competitiveness (±20 points)
    market_avg_price = market_data.get('average_price', 1500)
    price_ratio = unit.price / market_avg_price

    if price_ratio < 0.85:
        score += 20  # Excellent deal
    elif price_ratio < 0.95:
        score += 10  # Good value
    elif price_ratio > 1.15:
        score -= 15  # Overpriced
    elif price_ratio > 1.05:
        score -= 5   # Slightly expensive

    # 2. Listing Freshness (±15 points)
    days_listed = (datetime.utcnow() - unit.date_listed).days

    if days_listed < 3:
        score += 15  # Hot new listing (urgency)
    elif days_listed < 7:
        score += 10  # Recent
    elif days_listed < 14:
        score += 5   # Fresh
    elif days_listed > 45:
        score -= 15  # Stale, needs price adjustment
    elif days_listed > 30:
        score -= 10  # Getting stale

    # 3. Desirable Features (±20 points)
    high_value_amenities = {
        'parking': 7,
        'washer_dryer': 6,
        'pet_friendly': 5,
        'balcony': 4,
        'dishwasher': 3,
        'fitness_center': 4,
        'pool': 4,
        'ac': 3
    }

    amenity_score = 0
    for amenity in unit.amenities:
        amenity_lower = amenity.lower().replace(' ', '_')
        amenity_score += high_value_amenities.get(amenity_lower, 1)

    # Cap amenity bonus at 20 points
    score += min(20, amenity_score)

    # 4. Unit Size Appeal (±10 points)
    # 2+ bedrooms have higher demand
    if unit.bedrooms >= 3:
        score += 10
    elif unit.bedrooms == 2:
        score += 7
    elif unit.bedrooms == 1:
        score += 3

    # Multiple bathrooms increase appeal
    if unit.bathrooms >= 2.0:
        score += 5
    elif unit.bathrooms >= 1.5:
        score += 3

    # Square footage value
    price_per_sqft = unit.price / unit.square_feet
    market_avg_price_per_sqft = market_data.get('average_price_per_sqft', 1.5)

    if price_per_sqft < market_avg_price_per_sqft * 0.9:
        score += 5  # Great space value

    # 5. Location Desirability (±10 points)
    location = unit.location
    if isinstance(location, dict):
        city = location.get('city', '').lower()
        zip_code = location.get('zip', '')

        # Louisville prime zip codes (example)
        prime_zips = ['40202', '40204', '40206', '40207', '40222']
        if zip_code in prime_zips:
            score += 10

        # City-level desirability
        if 'louisville' in city:
            score += 5

    # Clamp score to 0-100 range
    final_score = max(0.0, min(100.0, score))

    return round(final_score, 2)


def calculate_score_breakdown(unit: models.Unit, market_data: Dict) -> Dict:
    """
    Calculate lead score with detailed breakdown
    Useful for explaining scoring to users

    Returns:
        Dictionary with score and component breakdown
    """
    breakdown = {
        'total_score': 50.0,
        'components': {
            'price_competitiveness': 0,
            'listing_freshness': 0,
            'desirable_features': 0,
            'unit_size_appeal': 0,
            'location_desirability': 0
        },
        'explanation': []
    }

    score = 50.0
    market_avg_price = market_data.get('average_price', 1500)
    price_ratio = unit.price / market_avg_price

    # Price Competitiveness
    if price_ratio < 0.85:
        price_points = 20
        breakdown['explanation'].append("Excellent pricing (20% below market)")
    elif price_ratio < 0.95:
        price_points = 10
        breakdown['explanation'].append("Good value pricing")
    elif price_ratio > 1.15:
        price_points = -15
        breakdown['explanation'].append("Overpriced (15% above market)")
    else:
        price_points = 0

    breakdown['components']['price_competitiveness'] = price_points
    score += price_points

    # Listing Freshness
    days_listed = (datetime.utcnow() - unit.date_listed).days
    if days_listed < 3:
        freshness_points = 15
        breakdown['explanation'].append(f"Brand new listing ({days_listed} days)")
    elif days_listed > 45:
        freshness_points = -15
        breakdown['explanation'].append(f"Stale listing ({days_listed} days)")
    else:
        freshness_points = max(-15, 15 - (days_listed // 3))

    breakdown['components']['listing_freshness'] = freshness_points
    score += freshness_points

    # Calculate final score
    total_score = calculate_lead_score(unit, market_data)
    breakdown['total_score'] = total_score

    return breakdown


def get_market_data(db: Session) -> Dict:
    """
    Calculate market statistics for lead scoring

    Returns:
        Dictionary with market averages
    """
    units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).all()

    if not units:
        return {
            'average_price': 1500,
            'average_price_per_sqft': 1.5,
            'total_units': 0
        }

    total_price = sum(u.price for u in units)
    total_sqft = sum(u.square_feet for u in units)

    return {
        'average_price': total_price / len(units),
        'average_price_per_sqft': total_price / total_sqft,
        'total_units': len(units)
    }


def recalculate_all_scores(db: Session) -> int:
    """
    Recalculate lead scores for all available units
    Should be run periodically (e.g., daily cron job)

    Returns:
        Number of units updated
    """
    market_data = get_market_data(db)
    units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).all()

    updated_count = 0
    for unit in units:
        new_score = calculate_lead_score(unit, market_data)
        if unit.lead_score != new_score:
            unit.lead_score = new_score
            unit.updated_at = datetime.utcnow()
            updated_count += 1

    db.commit()
    return updated_count
