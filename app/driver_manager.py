from database import add_violation
from datetime import datetime

# In-memory driver list (can expand this for Supabase if needed)
drivers = {
    "ABC-1234": {"id": "D001", "name": "John Doe", "email": "owner1@example.com"},
    "XYZ-5678": {"id": "D002", "name": "Jane Smith", "email": "owner2@example.com"}
}

def add_driver(plate, driver_id, name, email):
    if plate in drivers:
        return f"Driver with plate {plate} already exists."
    
    drivers[plate] = {"id": driver_id, "name": name, "email": email}
    
    # Automatically create a dummy violation for this driver
    violation = {
        "plate": plate,
        "owner": name,
        "speed": 120,  # Example dummy speed
        "limit": 100,
        "location": "Dummy Expressway 1",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paid": False
    }
    add_violation(violation)

    return f"Driver {name} added successfully with automatic violation."

def get_driver(plate):
    return drivers.get(plate, None)

def search_by_id(driver_id):
    for plate, info in drivers.items():
        if info["id"] == driver_id:
            return plate, info
    return None, None
