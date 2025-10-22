"""
Analytics Calculations
Real-time metrics for apartment leasing dashboard
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from datetime import datetime, timedelta
from collections import Counter
from . import models


def get_dashboard_analytics(db: Session) -> Dict:
    """
    Calculate comprehensive analytics for dashboard display

    Returns:
        Dictionary containing all key metrics
    """
    # Get unit counts by status
    total_units = db.query(models.Unit).count()
    available_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).count()
    leased_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.LEASED
    ).count()
    pending_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.PENDING
    ).count()

    # Calculate average days to lease
    avg_days_to_lease = calculate_average_days_to_lease(db)

    # Calculate lease conversion rate
    lease_conversion_rate = calculate_conversion_rate(
        leased_units,
        leased_units + available_units
    )

    # Calculate average price
    avg_price = db.query(func.avg(models.Unit.price)).scalar() or 0

    # Get most popular features
    popular_features = get_most_popular_features(db)

    # Get price trends (last 30 days)
    price_trends = get_price_trends(db, days=30)

    return {
        "total_units": total_units,
        "available_units": available_units,
        "leased_units": leased_units,
        "pending_units": pending_units,
        "average_days_to_lease": round(avg_days_to_lease, 1),
        "lease_conversion_rate": round(lease_conversion_rate, 2),
        "average_price": round(avg_price, 2),
        "most_popular_features": popular_features,
        "price_trends": price_trends
    }


def calculate_average_days_to_lease(db: Session) -> float:
    """
    Calculate average number of days from listing to lease

    Returns:
        Average days as float
    """
    leased_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.LEASED,
        models.Unit.date_leased.isnot(None)
    ).all()

    if not leased_units:
        return 0.0

    total_days = 0
    for unit in leased_units:
        days = (unit.date_leased - unit.date_listed).days
        total_days += days

    return total_days / len(leased_units)


def calculate_conversion_rate(leased_count: int, total_count: int) -> float:
    """
    Calculate lease conversion rate

    Args:
        leased_count: Number of leased units
        total_count: Total number of units (leased + available)

    Returns:
        Conversion rate as percentage (0-100)
    """
    if total_count == 0:
        return 0.0

    return (leased_count / total_count) * 100


def get_most_popular_features(db: Session, limit: int = 10) -> List[Dict]:
    """
    Analyze which amenities appear most in leased vs available units
    Higher ratio = more popular feature

    Returns:
        List of features with popularity metrics
    """
    leased_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.LEASED
    ).all()

    available_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).all()

    # Count amenity frequency
    leased_amenities = Counter()
    for unit in leased_units:
        if unit.amenities:
            leased_amenities.update(unit.amenities)

    available_amenities = Counter()
    for unit in available_units:
        if unit.amenities:
            available_amenities.update(unit.amenities)

    # Calculate popularity ratio
    feature_scores = []
    all_amenities = set(leased_amenities.keys()) | set(available_amenities.keys())

    for amenity in all_amenities:
        leased_count = leased_amenities.get(amenity, 0)
        available_count = available_amenities.get(amenity, 0)
        total_count = leased_count + available_count

        # Popularity ratio: leased / (leased + available)
        popularity_ratio = leased_count / total_count if total_count > 0 else 0

        feature_scores.append({
            "feature": amenity,
            "leased_count": leased_count,
            "available_count": available_count,
            "total_count": total_count,
            "popularity_ratio": round(popularity_ratio, 3)
        })

    # Sort by popularity ratio descending
    feature_scores.sort(key=lambda x: x['popularity_ratio'], reverse=True)

    return feature_scores[:limit]


def get_price_trends(db: Session, days: int = 30) -> List[Dict]:
    """
    Calculate average price trends over time

    Args:
        db: Database session
        days: Number of days to look back

    Returns:
        List of daily average prices
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    units = db.query(models.Unit).filter(
        models.Unit.date_listed >= cutoff_date
    ).all()

    # Group by date and calculate average
    price_by_date = {}
    for unit in units:
        date_key = unit.date_listed.date().isoformat()
        if date_key not in price_by_date:
            price_by_date[date_key] = []
        price_by_date[date_key].append(unit.price)

    # Calculate averages
    trends = []
    for date_str, prices in sorted(price_by_date.items()):
        avg_price = sum(prices) / len(prices)
        trends.append({
            "date": date_str,
            "average_price": round(avg_price, 2),
            "unit_count": len(prices)
        })

    return trends


def get_bedroom_distribution(db: Session) -> List[Dict]:
    """
    Get distribution of units by bedroom count

    Returns:
        List of bedroom counts with unit counts
    """
    results = db.query(
        models.Unit.bedrooms,
        func.count(models.Unit.id).label('count')
    ).group_by(models.Unit.bedrooms).all()

    return [
        {"bedrooms": bedrooms, "count": count}
        for bedrooms, count in results
    ]


def get_status_distribution(db: Session) -> Dict:
    """
    Get distribution of units by status

    Returns:
        Dictionary with status counts
    """
    statuses = db.query(
        models.Unit.status,
        func.count(models.Unit.id).label('count')
    ).group_by(models.Unit.status).all()

    return {
        status.value: count
        for status, count in statuses
    }


def get_city_distribution(db: Session) -> List[Dict]:
    """
    Get distribution of units by city
    Note: This requires JSON extraction (implementation varies by database)

    Returns:
        List of cities with unit counts
    """
    units = db.query(models.Unit).all()

    city_counts = Counter()
    for unit in units:
        if unit.location and isinstance(unit.location, dict):
            city = unit.location.get('city', 'Unknown')
            city_counts[city] += 1

    return [
        {"city": city, "count": count}
        for city, count in city_counts.most_common(10)
    ]


def get_performance_metrics(db: Session) -> Dict:
    """
    Calculate key performance indicators

    Returns:
        Dictionary with KPIs
    """
    total_units = db.query(models.Unit).count()
    leased_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.LEASED
    ).count()
    available_units = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).count()

    # Occupancy rate
    occupancy_rate = (leased_units / total_units * 100) if total_units > 0 else 0

    # Average lead score of available units
    avg_lead_score = db.query(func.avg(models.Unit.lead_score)).filter(
        models.Unit.status == models.UnitStatus.AVAILABLE
    ).scalar() or 0

    # Units leased in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_leases = db.query(models.Unit).filter(
        models.Unit.status == models.UnitStatus.LEASED,
        models.Unit.date_leased >= thirty_days_ago
    ).count()

    return {
        "occupancy_rate": round(occupancy_rate, 2),
        "average_lead_score": round(avg_lead_score, 2),
        "recent_leases_30d": recent_leases,
        "total_units": total_units,
        "available_units": available_units
    }
