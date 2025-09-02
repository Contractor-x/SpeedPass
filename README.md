#  SpeedPass Traffic System — A Beginner Python Project

**License Plate Detection & Automated Speed Violation Alerts (Dummy Version)**

---

## Basic Project Description

This is a beginner-friendly Python project simulating an intelligent traffic speed monitoring system. It reads license plates (dummy data), checks for speed violations, and sends automated alerts to the HQ and law enforcement (via dummy Gmail SMTP).

The system also simulates issuing fines to offenders and allows a basic web portal to display violation records and payment status (for demo purposes only).

** Top Features:**

* Reads dummy car plate numbers.
* Simulates over-speed detection.
* Sends automated email to "cops" if speed limit broken.
* Sends fine notification to offender via email.
* Stores vehicle & violation data in Supabase (dummy records).
* Simple website (Streamlit) to view offenses and pay fines (dummy payment logic).

---

##  Project Structure

```
speedpass-traffic-system/
├── app/
│   ├── main.py             # Main script to simulate traffic monitoring
│   ├── plate_reader.py     # Simulates license plate detection
│   ├── speed_checker.py    # Speed checking logic
│   ├── alert_system.py     # Email alert system (Gmail SMTP)
│   ├── database.py         # Supabase integration (dummy records)
│   └── payment.py          # Simulate fine payment logic
├── web/
│   ├── app.py              # Streamlit web portal
#├── .env                    # For storing API keys, credentials (excluded in .gitignore)
├── requirements.txt
├── README.md
└── LICENSE
```

---

##  Streamlit

* View list of recent violations (pulled from Supabase dummy DB).
* Search for your plate number to check fines.
* Dummy "Pay Fine" button that updates status in Supabase.

---

## Tech Stack

* **Python 3.11+**
* **Streamlit** for web interface.
* **dotenv** for secure environment variables.

---

##  Dummy Email Alert Example

```
Subject: SPEEDING VIOLATION ALERT — Vehicle Plate: ABC-1234

Dear Officer,

The vehicle with plate number ABC-1234 has been detected exceeding the speed limit.

Offense Details:
- Speed: 140 km/h
- Allowed Limit: 100 km/h
- Location: Dummy Expressway 1
- Time: 2025-06-24 14:35

Please take necessary action. A fine notice has been sent to the registered owner.

Regards,  
SpeedPass HQ Monitoring System
```

**Owner receives:**

```
Subject: Notice of Speed Violation — Plate: ABC-1234

Dear Vehicle Owner,

Our system detected your vehicle exceeding the speed limit.

- Speed: 140 km/h
- Allowed Limit: 100 km/h
- Fine: $100

Please visit the SpeedPass portal to view details and complete payment.

[Dummy Link to Pay Fine]

Failure to pay within 7 days may result in further action.

Regards,  
SpeedPass HQ
```

---

##  How to Run (Dev Setup)

```bash
git clone https://github.com/Contractor-x/speedpass-traffic-system.git
cd speedpass-traffic-system
pip install -r requirements.txt
```

1. Set up your `.env` with dummy Supabase keys and Gmail credentials.
2. Run `python app/main.py` to simulate system monitoring.
3. Run `streamlit run web/app.py` to open the portal.

---

## 🎯 Next Steps (For Beginners)

* Upgrade to real-time license plate reading (OpenCV, later).
* Integrate real payment systems.
* Add authentication to portal.
* Connect real hardware (if desired).

---

## 🔒 Disclaimer

**This is a beginner demo project. Not intended for real law enforcement use. Emails, databases, and payment logic are simulated.**



