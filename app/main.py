from plate_reader import read_plate
from speed_checker import is_speeding
from alert_system import send_email
from database import add_violation
import random
from datetime import datetime

while True:
    plate, owner = read_plate()
    speed = random.randint(80, 160)
    limit = 100
    location = "Dummy Expressway 1"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if is_speeding(speed, limit):
        violation = {
            "plate": plate,
            "owner": owner["name"],
            "speed": speed,
            "limit": limit,
            "location": location,
            "time": time_now,
            "paid": False
        }
        add_violation(violation)

        officer_msg = f"""SPEEDING VIOLATION ALERT — Vehicle Plate: {plate}

The vehicle with plate number {plate} has been detected exceeding the speed limit.

Offense Details:
- Speed: {speed} km/h
- Allowed Limit: {limit} km/h
- Location: {location}
- Time: {time_now}
"""
        send_email("police@example.com", f"SPEEDING ALERT — {plate}", officer_msg)

        owner_msg = f"""Notice of Speed Violation — Plate: {plate}

Dear {owner['name']},

Our system detected your vehicle exceeding the speed limit.

- Speed: {speed} km/h
- Allowed Limit: {limit} km/h
- Fine: $100
"""
        send_email(owner["email"], f"Notice of Speed Violation — {plate}", owner_msg)
        print(f"[ALERT] {plate} caught speeding at {speed} km/h")
    else:
        print(f"[OK] {plate} within limit at {speed} km/h")

    input("Press Enter to simulate next car...")
