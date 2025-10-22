#!/usr/bin/env python3
"""
Load seed data into database
Run this before starting the server
"""
import sys
import json
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import engine, Base, SessionLocal
from app.models import Unit, UnitStatus
from datetime import datetime

def load_seed_data():
    """Load seed data from JSON file into database"""

    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

    # Load seed data
    seed_file = Path(__file__).parent / "data" / "seed_data.json"

    if not seed_file.exists():
        print(f"❌ Seed data file not found: {seed_file}")
        return

    print(f"Loading seed data from {seed_file}...")

    with open(seed_file, 'r') as f:
        units_data = json.load(f)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Unit).count()

        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} units")
            response = input("Clear existing data and reload? (y/n): ")
            if response.lower() != 'y':
                print("Skipping seed data load")
                return

            # Clear existing data
            db.query(Unit).delete()
            db.commit()
            print("🗑️  Cleared existing data")

        # Insert seed data
        for unit_data in units_data:
            # Convert ISO date strings to datetime objects
            date_listed = datetime.fromisoformat(unit_data['date_listed'].replace('Z', '+00:00'))
            date_leased = None
            if unit_data.get('date_leased'):
                date_leased = datetime.fromisoformat(unit_data['date_leased'].replace('Z', '+00:00'))

            unit = Unit(
                id=unit_data['id'],
                property_name=unit_data['property_name'],
                unit_number=unit_data['unit_number'],
                bedrooms=unit_data['bedrooms'],
                bathrooms=unit_data['bathrooms'],
                square_feet=unit_data['square_feet'],
                price=unit_data['price'],
                status=UnitStatus(unit_data['status']),
                amenities=unit_data['amenities'],
                location=unit_data['location'],
                images=unit_data['images'],
                description=unit_data['description'],
                lead_score=unit_data['lead_score'],
                date_listed=date_listed,
                date_leased=date_leased
            )
            db.add(unit)

        db.commit()

        # Verify
        total_units = db.query(Unit).count()
        available = db.query(Unit).filter(Unit.status == UnitStatus.AVAILABLE).count()
        pending = db.query(Unit).filter(Unit.status == UnitStatus.PENDING).count()
        leased = db.query(Unit).filter(Unit.status == UnitStatus.LEASED).count()

        print(f"\n✅ Successfully loaded {total_units} units into database")
        print(f"   📊 Available: {available}")
        print(f"   ⏳ Pending: {pending}")
        print(f"   ✅ Leased: {leased}")

    except Exception as e:
        print(f"❌ Error loading seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_seed_data()
