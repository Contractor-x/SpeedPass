from database import add_owner, add_violation
from datetime import datetime

def add_driver(plate, driver_id, name, email):
    add_owner(plate, driver_id, name, email)
    
    violation = {
        "plate": plate,
        "owner": name,
        "speed": 120,
        "limit": 100,
        "location": "Dummy Expressway 1",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paid": False
    }
    add_violation(violation)
    return f"Driver {name} added with automatic violation."
