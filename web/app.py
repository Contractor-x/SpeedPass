import json
import random
import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_violations, owners, mark_fine_paid, add_owner, add_violation
from datetime import datetime

# ---- Cyberpunk CSS ----
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #000428, #004e92 100%);
}
[data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(120deg, #0f2027 0%, #2c5364 100%);
}
.cyberpunk-table {
    border-radius: 8px;
    overflow: hidden;
    background: rgba(10,10,30,0.97);
    color: #d4fc79;
    box-shadow: 0 0 30px #00ffe7, 0 0 10px #ff00cc;
}
.cyberpunk-card {
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #161a26 0%, #300048 100%);
    color: #d4fc79;
    border: 2px solid #00ffe7;
    box-shadow: 0 0 15px #00ffe7, 0 0 2px #ff00cc;
    transition: transform .2s, box-shadow .2s;
}
.cyberpunk-card:hover {
    transform: scale(1.025);
    box-shadow: 0 0 32px #ff00cc, 0 0 8px #00ffe7;
    border-color: #ff00cc;
}
.cyberpunk-label {
    font-weight: 700;
    color: #00ffe7;
    letter-spacing: 1px;
    margin-right: 4px;
}
a, a:visited {
    color: #ff00cc;
    text-decoration: none;
}
a:hover {
    color: #00ffe7;
    text-shadow: 0 0 8px #ff00cc;
}
h1, h2, h3, .stTitle {
    color: #fff;
    text-shadow: 0 0 10px #00ffe7, 0 0 4px #ff00cc;
}
</style>
""", unsafe_allow_html=True)

st.title("🚦 SpeedPass - Traffic Monitoring Dashboard")

# Load drivers data
with open("web/drivers.json") as f:
    drivers = json.load(f)
st.info(f"Total Registered Vehicles: {len(drivers)}")
st.info(f"Total Violations Recorded: {len(get_violations())}")

# === Registered Drivers Section ===
st.subheader("👥 Registered Drivers")

drivers_df = pd.DataFrame(drivers)
drivers_df = drivers_df.rename(columns={
    "Driver ID": "Plate/Driver ID",
    "id": "Short Name",
    "name": "Full Name",
    "email": "Email"
})

# Cyberpunk style DataFrame
st.markdown('<div class="cyberpunk-table">', unsafe_allow_html=True)
st.dataframe(
    drivers_df[["Plate/Driver ID", "Full Name", "Short Name", "Email"]],
    use_container_width=True,
    height=400
)
st.markdown('</div>', unsafe_allow_html=True)

# Card-based cyberpunk details
with st.expander("🟣 Show All Driver Details as Cyberpunk Cards"):
    for i, row in drivers_df.iterrows():
        st.markdown(
            f"""
            <div class="cyberpunk-card">
                <span class="cyberpunk-label">Plate/Driver ID:</span> {row['Plate/Driver ID']}<br>
                <span class="cyberpunk-label">Full Name:</span> {row['Full Name']}<br>
                <span class="cyberpunk-label">Short Name:</span> {row['Short Name']}<br>
                <span class="cyberpunk-label">Email:</span> <a href="mailto:{row['Email']}">{row['Email']}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# === Violations Section ===
violations = get_violations()
if violations:
    df = pd.DataFrame(violations)
    st.subheader("📊 Violations by Plate")
    fig = px.histogram(df, x="plate", title="Number of Violations per Plate",
                       color_discrete_sequence=["#ff00cc"])
    st.plotly_chart(fig)
    st.subheader("📋 Violation Records")
    st.dataframe(df, use_container_width=True)
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
