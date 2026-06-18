import sys
import os
import uuid

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models.crop import Crop
from app.models.scan import Scan
from app.ai.context_builder import ContextBuilder

def run_tests():
    app = create_app("testing")
    with app.app_context():
        # Setup schema
        db.create_all()

        crop1 = Crop(id=uuid.uuid4(), name="Tomato", supported=True)
        db.session.add(crop1)
        db.session.commit()

        print("--- Running ContextBuilder Tests ---")

        # Test 1: Supported prediction
        try:
            scan1 = Scan(id=uuid.uuid4(), crop_id=crop1.id, predicted_disease="Early Blight", confidence_score=0.85)
            scan1.crop = crop1
            context1 = ContextBuilder.build_disease_context(scan1)
            assert context1["disease"] == "Early Blight"
            print("Test 1 (Supported prediction -> Context generated): PASSED")
        except Exception as e:
            print(f"Test 1 FAILED: {str(e)}")

        # Test 2: Unsupported prediction
        try:
            scan2 = Scan(id=uuid.uuid4(), crop_id=crop1.id, predicted_disease="Unsupported", confidence_score=0.45)
            scan2.crop = crop1
            context2 = ContextBuilder.build_disease_context(scan2)
            assert context2["disease"] == "Unsupported"
            print("Test 2 (Unsupported prediction -> Context generated safely): PASSED")
        except Exception as e:
            print(f"Test 2 FAILED: {str(e)}")

        # Test 3: Missing selected plan
        try:
            context3 = ContextBuilder.build_disease_context(scan1, selected_plan=None)
            assert context3["selected_plan"] is None
            print("Test 3 (Missing selected plan -> Handled correctly): PASSED")
        except Exception as e:
            print(f"Test 3 FAILED: {str(e)}")

        # Test 4: Budget plan
        try:
            context4 = ContextBuilder.build_disease_context(scan1, selected_plan="BUDGET")
            assert context4["selected_plan"] == "BUDGET"
            print("Test 4 (Budget plan -> Included correctly): PASSED")
        except Exception as e:
            print(f"Test 4 FAILED: {str(e)}")

        # Test 5: Standard plan
        try:
            context5 = ContextBuilder.build_disease_context(scan1, selected_plan="STANDARD")
            assert context5["selected_plan"] == "STANDARD"
            print("Test 5 (Standard plan -> Included correctly): PASSED")
        except Exception as e:
            print(f"Test 5 FAILED: {str(e)}")

        # Test 6: Premium plan
        try:
            context6 = ContextBuilder.build_disease_context(scan1, selected_plan="PREMIUM")
            assert context6["selected_plan"] == "PREMIUM"
            print("Test 6 (Premium plan -> Included correctly): PASSED")
        except Exception as e:
            print(f"Test 6 FAILED: {str(e)}")

        # Test 7: Missing scan
        try:
            ContextBuilder.build_disease_context(None)
            print("Test 7 FAILED: Expected ValueError")
        except ValueError:
            print("Test 7 (Missing scan -> Raises ValueError): PASSED")

        # Test 8: Invalid confidence
        try:
            scan_invalid = Scan(id=uuid.uuid4(), crop_id=crop1.id, predicted_disease="Healthy", confidence_score=1.5)
            scan_invalid.crop = crop1
            ContextBuilder.build_disease_context(scan_invalid)
            print("Test 8 FAILED: Expected ValueError")
        except ValueError:
            print("Test 8 (Invalid confidence -> Raises ValueError): PASSED")

        # Test 9: Whitelist verification
        try:
            context9 = ContextBuilder.build_disease_context(scan1)
            assert set(context9.keys()) == {"crop", "disease", "confidence", "selected_plan"}
            print("Test 9 (Whitelist verification -> Only approved fields appear): PASSED")
        except Exception as e:
            print(f"Test 9 FAILED: {str(e)}")

        print("--- All Tests Completed ---")

if __name__ == "__main__":
    run_tests()
