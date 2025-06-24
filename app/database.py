# Holds all violations in memory
violations = []

# Holds all driver records
owners = {
    "ABC-1234": {"id": "D001", "email": "owner1@example.com", "name": "John Doe"},
    "XYZ-5678": {"id": "D002", "email": "owner2@example.com", "name": "Jane Smith"},
}

def add_violation(data):
    violations.append(data)

def get_violations():
    return violations

def mark_fine_paid(plate):
    for v in violations:
        if v["plate"] == plate:
            v["paid"] = True

def get_owner(plate):
    return owners.get(plate, {"email": "unknown@example.com", "name": "Unknown", "id": "N/A"})

def add_owner(plate, driver_id, name, email):
    owners[plate] = {"id": driver_id, "email": email, "name": name}
