#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta

properties = ["Highland Park", "Bardstown Lofts", "Old Louisville", "Downtown Living", "St. Matthews Place", "Crescent Hill", "Germantown Square", "Middletown Heights", "Cherokee Gardens", "Clifton Corner", "Butchertown Flats", "NuLu District", "Smoketown Commons", "Phoenix Hill", "Shelby Park"]
zips = ["40202", "40204", "40206", "40207", "40222"]
amenities_pool = ["parking", "washer_dryer", "dishwasher", "balcony", "patio", "pet_friendly", "ac", "heating", "hardwood_floors", "fitness_center", "pool", "storage", "walk_in_closet", "fireplace", "high_ceilings"]
statuses = ["available"] * 60 + ["pending"] * 15 + ["leased"] * 25

units = []
for i in range(100):
    bedrooms = random.choice([0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4])
    bathrooms = random.choice([1.0, 1.0, 1.5, 1.5, 2.0, 2.5])
    sqft = 500 + (bedrooms * 350) + random.randint(-150, 200)
    price = 750 + (bedrooms * 400) + random.randint(-100, 250)
    status = random.choice(statuses)
    property_name = random.choice(properties) + " Apartments"
    zip_code = random.choice(zips)

    date_listed = datetime(2025, random.randint(8, 10), random.randint(1, 28))
    date_leased = None
    if status == "leased":
        days_later = random.randint(5, 60)
        date_leased = date_listed + timedelta(days=days_later)

    unit = {
        "id": f"unit-{i+1:04d}",
        "property_name": property_name,
        "unit_number": f"{random.choice(['A','B','C','D'])}{random.randint(101, 512)}",
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "square_feet": sqft,
        "price": price,
        "status": status,
        "amenities": random.sample(amenities_pool, random.randint(3, 7)),
        "location": {
            "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Bardstown', 'Frankfort', 'Market', 'Broadway'])} {random.choice(['St', 'Ave', 'Rd'])}",
            "city": "Louisville",
            "state": "KY",
            "zip": zip_code,
            "lat": round(38.25 + random.uniform(-0.08, 0.08), 4),
            "lng": round(-85.76 + random.uniform(-0.08, 0.08), 4)
        },
        "images": [f"https://picsum.photos/seed/apt{i+1}img{j}/800/600" for j in range(1, random.randint(4, 7))],
        "description": f"{'Spacious' if sqft > 900 else 'Cozy'} {bedrooms}-bedroom apartment in {property_name}. Features {', '.join(random.sample(amenities_pool, 3))}. Great Louisville location.",
        "lead_score": 50.0,
        "date_listed": date_listed.isoformat() + "Z",
        "date_leased": date_leased.isoformat() + "Z" if date_leased else None
    }
    units.append(unit)

with open("seed_data.json", "w") as f:
    json.dump(units, f, indent=2)

print(f"Generated {len(units)} units")
print(f"Available: {sum(1 for u in units if u['status']=='available')}")
print(f"Pending: {sum(1 for u in units if u['status']=='pending')}")
print(f"Leased: {sum(1 for u in units if u['status']=='leased')}")
