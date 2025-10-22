#!/usr/bin/env python3
"""Quick seed data generator"""
import json
from datetime import datetime, timedelta
import random

units = []
statuses = ["available", "pending", "leased"]
amenities_pool = ["parking", "washer_dryer", "dishwasher", "balcony", "pet_friendly", "ac", "pool", "fitness_center"]

for i in range(100):
    bedrooms = random.choice([0, 1, 1, 2, 2, 2, 3])
    date_listed = (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat()

    unit = {
        "id": f"unit-{i:04d}",
        "property_name": f"Property {i % 15 + 1}",
        "unit_number": f"{random.choice(['A','B','C'])}{random.randint(101, 512)}",
        "bedrooms": bedrooms,
        "bathrooms": random.choice([1.0, 1.5, 2.0, 2.5]),
        "square_feet": 600 + (bedrooms * 300) + random.randint(-100, 200),
        "price": 800 + (bedrooms * 400) + random.randint(-200, 300),
        "status": random.choice(statuses),
        "amenities": random.sample(amenities_pool, random.randint(3, 6)),
        "location": {
            "address": f"{random.randint(100, 9999)} Main St",
            "city": "Louisville",
            "state": "KY",
            "zip": random.choice(["40202", "40204", "40206", "40207"]),
            "lat": 38.25 + random.uniform(-0.05, 0.05),
            "lng": -85.76 + random.uniform(-0.05, 0.05)
        },
        "images": [f"https://picsum.photos/seed/apt{i}/800/600"],
        "description": f"Spacious {bedrooms}-bedroom apartment with great amenities.",
        "lead_score": 50.0,
        "date_listed": date_listed,
        "date_leased": None
    }
    units.append(unit)

with open("seed_data.json", "w") as f:
    json.dump(units, f, indent=2)

print(f"Generated {len(units)} units")
