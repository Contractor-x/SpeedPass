import json
import random
import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_violations, owners, mark_fine_paid, add_owner, add_violation
from datetime import datetime

st.title("🚦 SpeedPass - Traffic Monitoring Dashboard")

# Load drivers data
with open("web/drivers.json") as f:
    drivers = json.load(f)

# Display info
st.info(f"Total Registered Vehicles: {len(drivers)}")
st.info(f"Total Violations Recorded: {len(get_violations())}")

# === Registered Drivers Section ===
st.subheader("👥 Registered Drivers")

drivers_df = pd.DataFrame(drivers)

# Only use columns that exist
display_names = {
    "Driver ID": "Plate/Driver ID",
    "name": "Full Name",
    "id": "Short Name",
    "email": "Email"
}
existing_cols = [k for k in display_names if k in drivers_df.columns]

if existing_cols:
    drivers_df_display = drivers_df[existing_cols].rename(columns={k: v for k, v in display_names.items() if k in existing_cols})
    st.dataframe(drivers_df_display, use_container_width=True, height=400)
else:
    st.info("No driver data available.")

with st.expander("Show All Driver Details"):
    for _, row in drivers_df.iterrows():
        st.write(
            f"**Plate/Driver ID:** {row.get('Driver ID', '')}\n"
            f"**Full Name:** {row.get('name', '')}\n"
            f"**Short Name:** {row.get('id', '')}\n"
            f"**Email:** {row.get('email', '')}\n"
            "---"
        )

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

st.subheader("💳 Pay Fine")
plate = st.text_input("Enter Driver Plate Number to Pay Fine:")
if st.button("Pay Fine"):
    mark_fine_paid(plate)
    st.success(f"Fine marked as paid for {plate}")

st.sidebar.title("🚗 Add New Driver (Auto Violation)")
new_plate = st.sidebar.text_input("Plate Number")
driver_id = st.sidebar.text_input("Driver ID")
name = st.sidebar.text_input("Driver Name")
email = st.sidebar.text_input("Email Address")

if st.sidebar.button("Add Driver"):
    add_owner(new_plate, driver_id, name, email)
    speed = random.randint(80, 420)
    locations = [
        "Dummy Expressway 1",
        "Main Avenue",
        "Sunset Boulevard",
        "Coastal Road",
        "Greenbelt Parkway",
        "Maple Street",
        "Central Highway",
        "Riverfront Drive",
        "Mountain Pass",
        "Lakeside Road",
        "Industrial Zone Bypass",
        "Airport Express",
        "University Loop",
        "Old Town Road",
        "Harbor Street",
        "Forest Trail",
        "Metro Link",
        "East End Boulevard",
        "Westgate Drive",
        "Downtown Connector"
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

def add_violation(data, fine=None):
    # Set fine to a random amount between 2,000 and 10,000,000 if not provided
    if fine is None:
        fine = random.randint(2000, 10000000)
    data["fine"] = fine
    violations.append(data)
    save_data()
