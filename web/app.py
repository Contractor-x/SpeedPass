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
st.info(f"Total Registered Vehicles: {len(drivers)}")
st.info(f"Total Violations Recorded: {len(get_violations())}")

# === Registered Drivers Section ===
st.subheader("👥 Registered Drivers")
display_cols = [c for c in ["Driver ID", "name", "id", "email"] if c in drivers_df.columns]
display_names = {
    "Driver ID": "Plate/Driver ID",
    "name": "Full Name",
    "id": "Short Name",
    "email": "Email"
}
drivers_df_display = drivers_df[display_cols].rename(columns=display_names)

st.dataframe(
    drivers_df_display,
    use_container_width=True,
    height=400
)

with st.expander("🟣 Show All Driver Details as Cyberpunk Cards"):
    for _, row in drivers_df.iterrows():
        st.markdown(
            f"""
            <div class="cyberpunk-card">
                <span class="cyberpunk-label">Plate/Driver ID:</span> {row.get('Driver ID', '')}<br>
                <span class="cyberpunk-label">Full Name:</span> {row.get('name', '')}<br>
                <span class="cyberpunk-label">Short Name:</span> {row.get('id', '')}<br>
                <span class="cyberpunk-label">Email:</span> <a href="mailto:{row.get('email', '')}">{row.get('email', '')}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# Show as a beautiful interactive table
drivers_df = pd.DataFrame(drivers)
drivers_df = drivers_df.rename(columns={
    "Driver ID": "Plate/Driver ID",
    "id": "Short Name",
    "name": "Full Name",
    "email": "Email"
})

st.dataframe(
    drivers_df[["Plate/Driver ID", "Full Name", "Short Name", "Email"]],
    use_container_width=True,
    height=400
)

with st.expander("Show All Driver Details as Cards"):
    for i, row in drivers_df.iterrows():
        st.markdown(
            f"""
            <div style="border:1px solid #eee; border-radius:10px; padding:10px; margin-bottom:10px; background: #fafbfc;">
                <b>Plate/Driver ID:</b> {row['Plate/Driver ID']}<br>
                <b>Full Name:</b> {row['Full Name']}<br>
                <b>Short Name:</b> {row['Short Name']}<br>
                <b>Email:</b> <a href="mailto:{row['Email']}">{row['Email']}</a>
            </div>
            """,
            unsafe_allow_html=True
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
    # Set fine to a random amount between 10,000 and 30,000 if not provided
    if fine is None:
        fine = random.randint(2000, 10000000)
    data["fine"] = fine
    violations.append(data)
    save_data()
