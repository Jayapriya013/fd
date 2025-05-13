import streamlit as st
import pandas as pd
import numpy as np

st.title("🛬 Flight Arrival Delay Predictor (Dataset-Based)")

# ✅ Load dataset from GitHub
url = "https://raw.githubusercontent.com/Jayapriya013/fd/main/final_airline_times_HHMM%20(2).csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# Show sample
st.write("### 📄 Sample of the Dataset")
st.dataframe(df.head())

# ✅ Dropdowns for more filtering
st.subheader("📝 Enter Flight Info")

# Get unique sorted values from dataset
origins = sorted(df['Origin'].dropna().unique())
destinations = sorted(df['Dest'].dropna().unique())
carriers = sorted(df['Carrier'].dropna().unique())
years = sorted(df['Year'].dropna().unique())
airport_col = "OriginAirportName" if "OriginAirportName" in df.columns else None

origin = st.selectbox("🛫 Origin", origins)
destination = st.selectbox("🛬 Destination", destinations)
carrier = st.selectbox("✈️ Carrier", carriers)
year = st.selectbox("📅 Year", years)

if airport_col:
    airports = sorted(df[airport_col].dropna().unique())
    airport_name = st.selectbox("🏢 Airport Name", airports)
else:
    airport_name = None

# ✅ Time inputs
sched_dep = st.text_input("⏰ Scheduled Departure Time (HH:MM)", "")
actual_arr = st.text_input("⏱️ Actual Arrival Time (HH:MM)", "")

# ✅ Time conversion function
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

# ✅ Predict Delay
if st.button("🔎 Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    actual_arr_min = convert_to_minutes(actual_arr)

    if np.isnan(sched_dep_min) or np.isnan(actual_arr_min):
        st.error("❌ Please enter valid times in HH:MM format.")
    else:
        # Filter using all selected details
        match = df[
            (df['Origin'] == origin) &
            (df['Dest'] == destination) &
            (df['Carrier'] == carrier) &
            (df['Year'] == year)
        ]
        
        if airport_name:
            match = match[match[airport_col] == airport_name]

        if match.empty:
            st.error("❌ No matching flight found in the dataset.")
        else:
            # Match with exact scheduled departure
            exact_match = match[match['ScheduledDeparture'] == sched_dep]

            if exact_match.empty():
                st.warning("⚠️ No exact departure match. Showing first match based on other filters.")
                match_row = match.iloc[0]
            else:
                match_row = exact_match.iloc[0]

            sched_arr = match_row['ScheduledArrival']
            sched_arr_min = convert_to_minutes(sched_arr)

            if np.isnan(sched_arr_min):
                st.error("❌ Invalid Scheduled Arrival Time in dataset.")
            else:
                delay = actual_arr_min - sched_arr_min

                if delay > 15:
                    st.error(f"🛑 Flight delayed by {delay} minutes.")
                else:
                    st.success("✅ Flight is on time or within 15 minutes.")
