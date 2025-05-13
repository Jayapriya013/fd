import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Flight Delay Predictor", layout="wide")

# Title
st.title("✈️ Flight Arrival Delay Predictor (Dataset-Based)")

# ✅ Raw GitHub CSV URL
url = "https://raw.githubusercontent.com/Jayapriya013/fd/main/final_airline_times_HHMM%20(2).csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# Show sample data
st.write("### 🧾 Sample of the Dataset")
st.dataframe(df.head())

# Dropdown values
origins = sorted(df['origin'].dropna().unique())
destinations = sorted(df['destination'].dropna().unique())
carriers = sorted(df['carrier'].dropna().unique())
years = sorted(df['year'].dropna().unique())

# Flight Info Inputs
st.subheader("📝 Enter Flight Info")

col1, col2, col3, col4 = st.columns(4)
with col1:
    origin = st.selectbox("Origin Airport", origins)
with col2:
    destination = st.selectbox("Destination Airport", destinations)
with col3:
    carrier = st.selectbox("Carrier", carriers)
with col4:
    year = st.selectbox("Year", years)

# Time Inputs
sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "")
actual_arr = st.text_input("Actual Arrival Time (HH:MM)", "")

# Time conversion function
def convert_to_minutes(time_str):
    try:
        if ":" not in time_str:
            raise ValueError
        h, m = map(int, time_str.strip().split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except:
        return np.nan

# Predict Button
if st.button("🔍 Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    actual_arr_min = convert_to_minutes(actual_arr)

    if np.isnan(sched_dep_min) or np.isnan(actual_arr_min):
        st.error("❌ Please enter valid times in HH:MM format.")
    else:
        # Filter dataset by selected fields
        match = df[
            (df['origin'] == origin) &
            (df['destination'] == destination) &
            (df['carrier'] == carrier) &
            (df['year'] == year) &
            (df['scheduled_departure_time'] == sched_dep)
        ]

        if match.empty:
            st.error("❌ No matching flight found in the dataset.")
        else:
            sched_arr = match.iloc[0]['scheduled_arrival_time']
            sched_arr_min = convert_to_minutes(sched_arr)

            if np.isnan(sched_arr_min):
                st.error("❌ Invalid Scheduled Arrival Time in dataset.")
            else:
                arrival_delay = actual_arr_min - sched_arr_min

                if arrival_delay > 15:
                    st.error(f"🛑 Flight is **Delayed** by {arrival_delay} minutes.")
                else:
                    st.success("✅ Flight is **On Time**.")
