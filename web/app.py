import streamlit as st
import pandas as pd
from app.driver_manager import add_driver, search_by_id, drivers
from app.database import get_violations, mark_fine_paid
import plotly.express as px

st.title("🚦 SpeedPass Traffic System - Dashboard")

# Main Violations Display
data = get_violations()
df = pd.DataFrame(data)

if df.empty:
    st.info("No violations yet.")
else:
    st.subheader("📊 Offender Statistics")
    fig = px.histogram(df, x="plate", title="Violations by Plate")
    st.plotly_chart(fig)

    st.subheader("📋 Violation Records")
    st.dataframe(df)

    st.subheader("💳 Pay Fine")
    plate_input = st.text_input("Enter your Plate Number to Pay Fine:")
    if st.button("Pay Fine"):
        mark_fine_paid(plate_input)
        st.success(f"Fine marked as paid for {plate_input}. Refresh page to see updates.")

# Sidebar - Driver Management
st.sidebar.title("🚗 Driver Management")

if st.sidebar.button("View All Drivers"):
    st.sidebar.dataframe(pd.DataFrame(drivers).T)

st.sidebar.subheader("Add New Driver (Triggers Violation)")
plate = st.sidebar.text_input("Plate Number")
driver_id = st.sidebar.text_input("Driver ID")
name = st.sidebar.text_input("Name")
email = st.sidebar.text_input("Email")

if st.sidebar.button("Add Driver & Violate"):
    msg = add_driver(plate, driver_id, name, email)
    st.sidebar.success(msg)

st.sidebar.subheader("Search by Driver ID")
search_id = st.sidebar.text_input("Enter Driver ID")
if st.sidebar.button("Search"):
    plate_found, info = search_by_id(search_id)
    if info:
        st.sidebar.info(f"Found: {info['name']} with Plate {plate_found}")
    else:
        st.sidebar.warning("Driver ID not found.")

