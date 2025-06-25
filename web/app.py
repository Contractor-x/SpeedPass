import json
import os
import random
import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_violations, owners, mark_fine_paid, add_owner, add_violation
from datetime import datetime

st.title("🚦 SpeedPass - Traffic Monitoring Dashboard")

DRIVER_FILE = "app/drivers.json"  # Correct path if drivers.json is inside app folder

# Load drivers as dict safely
if os.path.exists(DRIVER_FILE):
    with open(DRIVER_FILE) as f:
        try:
            drivers_data = json.load(f)
        except:
            drivers_data = {}
else:
    drivers_data = {}

if not isinstance(drivers_data, dict):
    drivers_data = {}

# Convert dict to list for DataFrame display
drivers_list = []
for plate, info in drivers_data.items():
    drivers_list.append({
        "Plate": plate,
        "Driver ID": info.get("id", ""),
        "Name": info.get("name", ""),
        "Email": info.get("email", "")
    })

st.info(f"Total Registered Vehicles: {len(drivers_list)}")
st.info(f"Total Violations Recorded: {len(get_violations())}")

# === Registered Drivers Section ===
st.subheader("👥 Registered Drivers")

drivers_df = pd.DataFrame(drivers_list)
if not drivers_df.empty:
    st.dataframe(drivers_df, use_container_width=True, height=400)
else:
    st.info("No driver data available.")

with st.expander("Show All Driver Details"):
    for row in drivers_list:
        st.write(f"**Plate:** {row.get('Plate')}")
        st.write(f"**Driver ID:** {row.get('Driver ID')}")
        st.write(f"**Name:** {row.get('Name')}")
        st.write(f"**Email:** {row.get('Email')}")
        st.markdown("---")

# === Violations Section ===
violations = get_violations()
if violations:
    df = pd.DataFrame(violations)
    st.subheader("📊 Violations by Plate")
    fig = px.histogram(df, x="plate", title="Number of Violations per Plate")
    st.plotly_chart(fig)
    st.subheader("📋 Violation Records")
    st.dataframe(df)
else:
    st.info("No violations recorded yet.")

# === Fine Payment Section ===
st.subheader("💳 Pay Fine")
plate = st.text_input("Enter Driver Plate Number to Pay Fine:")
if st.button("Pay Fine"):
    mark_fine_paid(plate)
    st.success(f"Fine marked as paid for {plate}")

# === Add New Driver Section ===
st.sidebar.title("🚗 Add New Driver (Auto Violation)")
new_plate = st.sidebar.text_input("Plate Number")
driver_id = st.sidebar.text_input("Driver ID")
name = st.sidebar.text_input("Driver Name")
email = st.sidebar.text_input("Email Address")

if st.sidebar.button("Add Driver"):
    drivers_data[new_plate] = {"id": driver_id, "email": email, "name": name}

    with open(DRIVER_FILE, "w") as f:
        json.dump(drivers_data, f, indent=4)

    add_owner(new_plate, driver_id, name, email)
    speed = random.randint(80, 420)
    locations = [
        "Dummy Expressway 1", "Main Avenue", "Sunset Boulevard",
        "Coastal Road", "Greenbelt Parkway", "Maple Street",
        "Central Highway", "Riverfront Drive", "Mountain Pass",
        "Lakeside Road", "Industrial Zone Bypass", "Airport Express",
        "University Loop", "Old Town Road", "Harbor Street",
        "Forest Trail", "Metro Link", "East End Boulevard",
        "Westgate Drive", "Downtown Connector"
    ]
    location = random.choice(locations)
    violation = {
        "plate": new_plate,
        "owner": name,
        "speed": speed,
        "limit": 100,
        "location": location,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paid": False
    }
    add_violation(violation)
    st.sidebar.success(f"Driver {name} added with automatic violation.")
