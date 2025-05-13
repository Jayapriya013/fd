import streamlit as st
import pandas as pd
import numpy as np

# Title
st.title("✈️ Flight Arrival Delay Predictor (Dataset-Based)")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv
    import pandas as pd
import streamlit as st

# Correct raw URL from your GitHub
import streamlit as st
import pandas as pd

# ✅ Correct raw GitHub CSV URL
url = "https://raw.githubusercontent.com/Jayapriya013/fd/main/final_airline_times_HHMM%20(2).csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

st.title("🛬 Flight Arrival Delay Predictor (Dataset-Based)")

st.write("### Sample Data")
st.dataframe(df.head())


# User Inputs
st.subheader("Enter Flight Details")

sched_dep = st.text_input("Scheduled Departure Time (HH:MM)", "")
actual_arr = st.text_input("Actual Arrival Time (HH:MM)", "")

# Convert HH:MM to total minutes from midnight
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

if st.button("Predict Delay"):
    sched_dep_min = convert_to_minutes(sched_dep)
    actual_arr_min = convert_to_minutes(actual_arr)

    if np.isnan(sched_dep_min) or np.isnan(actual_arr_min):
        st.error("❌ Please enter valid times in HH:MM format.")
    else:
        # Search dataset for matching Scheduled Departure Time
        match = df[df['ScheduledDeparture'] == sched_dep]

        if match.empty:
            st.error("❌ No matching flight found in the dataset.")
        else:
            sched_arr = match.iloc[0]['ScheduledArrival']
            sched_arr_min = convert_to_minutes(sched_arr)

            if np.isnan(sched_arr_min):
                st.error("❌ Invalid Scheduled Arrival Time in dataset.")
            else:
                arrival_delay = actual_arr_min - sched_arr_min

                if arrival_delay > 15:
                    st.error(f"🛑 Delayed by {arrival_delay} minutes.")
                else:
                    st.success("✅ On-Time.")
