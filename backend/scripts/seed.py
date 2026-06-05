"""
AgroGuard Backend - Database Seeding Script

This script seeds the PostgreSQL database with the default V1 supported crops
(Tomato and Potato) as specified in PRD.md §5 and Architecture.md.

To guarantee idempotency, it checks for existing crop names and updates
their properties if they differ, rather than blindly inserting duplicates.

This is the single source of truth for the seeding logic. The Flask CLI wrapper
calls run_seed() to execute this logic.

Usage:
    # Run from the backend/ directory:
    venv/Scripts/python scripts/seed.py
"""

from __future__ import annotations

import os
import sys
from dotenv import load_dotenv

# Ensure the backend root is in the Python search path so 'app' imports correctly.
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

# Load env variables before importing anything from the app package.
# This ensures that class-level configuration variables (evaluated at import time)
# correctly read from the environment instead of falling back to default values.
load_dotenv(os.path.join(backend_root, ".env"))

from app.database import db
from app.models.crop import Crop


def run_seed(verbose: bool = True) -> None:
    """
    Seeds the crops table with the baseline supported crops.
    Must be called within an active Flask application context.
    
    Ensures idempotency:
      - Inserts the crop if it does not exist.
      - Updates the supported flag if the crop exists but differs.
      - Skips insertion if both match.
    """
    # V1 Supported Crops baseline definitions
    default_crops = [
        {"name": "Tomato", "supported": True},
        {"name": "Potato", "supported": True},
    ]

    seeded_count = 0
    updated_count = 0
    skipped_count = 0

    for crop_data in default_crops:
        # Search by unique name
        existing_crop = Crop.query.filter_by(name=crop_data["name"]).first()

        if not existing_crop:
            # Create a new crop entry
            new_crop = Crop(
                name=crop_data["name"],
                supported=crop_data["supported"]
            )
            db.session.add(new_crop)
            seeded_count += 1
            print(f" -> [INSERT] '{crop_data['name']}' (supported={crop_data['supported']})")
        else:
            # Update supported flag if it has diverged
            if existing_crop.supported != crop_data["supported"]:
                existing_crop.supported = crop_data["supported"]
                db.session.add(existing_crop)
                updated_count += 1
                print(f" -> [UPDATE] '{crop_data['name']}' supported status to {crop_data['supported']}")
            else:
                skipped_count += 1
                if verbose:
                    print(f" -> [SKIP]   '{crop_data['name']}' (already exists & correct)")

    # Commit only if database writes occurred
    if seeded_count > 0 or updated_count > 0:
        db.session.commit()
        print("Success: Database updated. Seeding transaction committed.")
    else:
        print("No schema updates required. Database is already up-to-date.")

    print(f"Summary: Seeding completed. (Created: {seeded_count}, Updated: {updated_count}, Skipped: {skipped_count})")


if __name__ == "__main__":
    from app import create_app

    env = os.getenv("FLASK_ENV", "development")
    app = create_app(env)

    print(f"[{env.upper()}] Seeding supported crops via standalone script...")
    with app.app_context():
        try:
            run_seed(verbose=True)
        except Exception as e:
            print(f"Error seeding database: {e}", file=sys.stderr)
            sys.exit(1)
