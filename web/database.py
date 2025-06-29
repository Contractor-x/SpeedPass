import json
import os

DRIVER_FILE = os.path.join(os.path.dirname(__file__), "drivers.json")
VIOLATION_FILE = os.path.join(os.path.dirname(__file__), "violations.json")

# Defensive loading for owners
owners = {}
if os.path.exists(DRIVER_FILE):
    with open(DRIVER_FILE) as f:
        loaded_owners = json.load(f)
        # Auto-convert list to dict if needed
        if isinstance(loaded_owners, list):
            # Use "Driver ID" as the plate key
            owners = {
                item["Driver ID"]: {
                    "id": item.get("Driver ID", ""),  # Use Driver ID as id
                    "email": item.get("email", ""),
                    "name": item.get("name", "")
                }
                for item in loaded_owners if "Driver ID" in item
            }
        elif isinstance(loaded_owners, dict):
            owners = loaded_owners
else:
    owners = {}

# Defensive loading for violations
if os.path.exists(VIOLATION_FILE):
    with open(VIOLATION_FILE) as f:
        violations = json.load(f)
else:
    violations = []

def save_data():
    with open(DRIVER_FILE, "w") as f:
        json.dump(owners, f, indent=4)
    with open(VIOLATION_FILE, "w") as f:
        json.dump(violations, f, indent=4)

def add_owner(plate, driver_id, name, email):
    owners[plate] = {"id": driver_id, "email": email, "name": name}
    save_data()

def get_owner(plate):
    return owners.get(plate, {"email": "unknown@example.com", "name": "Unknown", "id": "N/A"})

def add_violation(data):
    violations.append(data)
    save_data()

def get_violations():
    return violations

def mark_fine_paid(plate):
    for v in violations:
        if v.get("plate") == plate:
            v["paid"] = True
    save_data()
