"""
Seed Data Generator
Creates realistic apartment unit data for demo purposes
"""

import json
import random
from datetime import datetime, timedelta
import uuid

# Louisville, KY neighborhoods and properties
PROPERTIES = [
    ("Highland Park Apartments", "40204"),
    ("Bardstown Road Lofts", "40204"),
    ("Old Louisville Manor", "40208"),
    ("Downtown Living", "40202"),
    ("St. Matthews Place", "40207"),
    ("Crescent Hill Residences", "40206"),
    ("Germantown Square", "40212"),
    ("Middletown Heights", "40222"),
    ("Cherokee Gardens", "40204"),
    ("Clifton Corner", "40206"),
    ("Butchertown Flats", "40206"),
    ("NuLu District Living", "40202"),
    ("Smoketown Commons", "40203"),
    ("Phoenix Hill Apartments", "40203"),
    ("Shelby Park Place", "40217")
]

STREET_NAMES = [
    "Bardstown Road", "Frankfort Avenue", "Main Street", "Market Street",
    "Broadway", "Baxter Avenue", "Preston Street", "4th Street",
    "Grinstead Drive", "Cherokee Road", "Eastern Parkway", "Spring Street",
    "Story Avenue", "Lexington Road", "Brownsboro Road"
]

# Available amenities
AMENITIES_POOL = [
    "parking", "washer_dryer", "dishwasher", "balcony", "patio",
    "pet_friendly", "ac", "heating", "hardwood_floors", "carpet",
    "fitness_center", "pool", "storage", "walk_in_closet", "fireplace",
    "high_ceilings", "stainless_appliances", "granite_counters"
]

UNIT_STATUSES = ["available", "pending", "leased"]


def generate_random_date(days_ago_min=1, days_ago_max=90):
    """Generate random past date"""
    days_ago = random.randint(days_ago_min, days_ago_max)
    return datetime.utcnow() - timedelta(days=days_ago)


def generate_unit():
    """Generate a single apartment unit with realistic data"""

    # Select property
    property_name, zip_code = random.choice(PROPERTIES)

    # Unit specifications
    bedrooms = random.choices([0, 1, 2, 3, 4], weights=[5, 30, 40, 20, 5])[0]
    bathrooms = random.choice([1.0, 1.5, 2.0, 2.5, 3.0])

    # Square footage based on bedrooms
    base_sqft = {0: 450, 1: 650, 2: 950, 3: 1300, 4: 1800}[bedrooms]
    square_feet = base_sqft + random.randint(-100, 200)

    # Price based on bedrooms and location
    base_price = {0: 750, 1: 950, 2: 1350, 3: 1750, 4: 2200}[bedrooms]

    # Prime zip codes cost more
    prime_zips = ["40202", "40204", "40206", "40207", "40222"]
    if zip_code in prime_zips:
        base_price += random.randint(100, 300)
    else:
        base_price += random.randint(-100, 100)

    price = base_price

    # Status distribution (60% available, 25% leased, 15% pending)
    status = random.choices(UNIT_STATUSES, weights=[60, 15, 25])[0]

    # Amenities (3-8 random amenities)
    num_amenities = random.randint(3, 8)
    amenities = random.sample(AMENITIES_POOL, num_amenities)

    # Location
    street_number = random.randint(100, 9999)
    street_name = random.choice(STREET_NAMES)
    location = {
        "address": f"{street_number} {street_name}",
        "city": "Louisville",
        "state": "KY",
        "zip": zip_code,
        "lat": round(38.2527 + random.uniform(-0.1, 0.1), 4),
        "lng": round(-85.7585 + random.uniform(-0.1, 0.1), 4)
    }

    # Images (mock image URLs)
    image_count = random.randint(3, 8)
    images = [
        f"https://picsum.photos/seed/{uuid.uuid4().hex[:8]}/800/600"
        for _ in range(image_count)
    ]

    # Description
    bedroom_text = {
        0: "studio",
        1: "1-bedroom",
        2: "2-bedroom",
        3: "3-bedroom",
        4: "4-bedroom"
    }[bedrooms]

    descriptions = [
        f"Spacious {bedroom_text} apartment in {property_name}. Features include {', '.join(amenities[:3])}. Great location near shops and restaurants.",
        f"Modern {bedroom_text} unit with {square_feet} sq ft of living space. Recently updated with new appliances and flooring. Pet-friendly building.",
        f"Charming {bedroom_text} apartment in Louisville's vibrant {property_name} community. Close to public transit and downtown.",
        f"Beautiful {bedroom_text} home with {bathrooms} baths. Enjoy amenities like {', '.join(amenities[:2])}. Available immediately.",
        f"Updated {bedroom_text} apartment featuring {', '.join(amenities[:4])}. Quiet neighborhood with easy highway access."
    ]
    description = random.choice(descriptions)

    # Dates
    date_listed = generate_random_date(1, 90)
    date_leased = None

    if status == "leased":
        # Leased 1-60 days after listing
        days_to_lease = random.randint(1, 60)
        date_leased = date_listed + timedelta(days=days_to_lease)

    # Unit number
    building = random.choice(['A', 'B', 'C', 'D'])
    floor = random.randint(1, 12)
    unit_num = random.randint(1, 20)
    unit_number = f"{building}{floor}{unit_num:02d}"

    return {
        "id": str(uuid.uuid4()),
        "property_name": property_name,
        "unit_number": unit_number,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "square_feet": square_feet,
        "price": price,
        "status": status,
        "amenities": amenities,
        "location": location,
        "images": images,
        "description": description,
        "lead_score": 50.0,  # Will be recalculated by backend
        "date_listed": date_listed.isoformat(),
        "date_leased": date_leased.isoformat() if date_leased else None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


def generate_seed_data(count=100):
    """Generate multiple apartment units"""
    units = [generate_unit() for _ in range(count)]
    return units


if __name__ == "__main__":
    # Generate 100 units
    units = generate_seed_data(100)

    # Save to JSON file
    output_file = "seed_data.json"
    with open(output_file, 'w') as f:
        json.dump(units, f, indent=2)

    print(f"✅ Generated {len(units)} apartment units")
    print(f"💾 Saved to {output_file}")

    # Print statistics
    status_counts = {}
    for unit in units:
        status = unit['status']
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"\n📊 Status Distribution:")
    for status, count in status_counts.items():
        print(f"   {status}: {count}")

    avg_price = sum(u['price'] for u in units) / len(units)
    print(f"\n💰 Average Price: ${avg_price:.2f}")
