import streamlit as st
import pandas as pd

# Helper function to convert HHMM to minutes
def hhmm_to_minutes(hhmm):
    hhmm = str(hhmm).zfill(4)
    hours = int(hhmm[:2])
    minutes = int(hhmm[2:])
    return hours * 60 + minutes

# Main app
st.title("Flight Delay Predictor 🚀")

uploaded_file = st.file_uploader('/content/drive/My Drive/flight delay prediction/final_airline_times_HHMM.csv') 

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display raw data
    st.subheader("Raw Data Preview")
    st.write(df.head())

    # Ensure required columns are present
    required_cols = ['Actual Arrival Time', 'Scheduled Departure Time', 'Actual Departure Time']
    if not all(col in df.columns for col in required_cols):
        st.error(f"CSV must contain columns: {required_cols}")
    else:
        # Convert times to minutes
        df['Scheduled Departure (mins)'] = df['Scheduled Departure Time'].apply(hhmm_to_minutes)
        df['Actual Departure (mins)'] = df['Actual Departure Time'].apply(hhmm_to_minutes)
        df['Actual Arrival (mins)'] = df['Actual Arrival Time'].apply(hhmm_to_minutes)

        # Calculate delay (as difference between actual and scheduled departure)
        df['Departure Delay (mins)'] = df['Actual Departure (mins)'] - df['Scheduled Departure (mins)']

        # Handle crossing midnight (negative delays)
        df['Departure Delay (mins)'] = df['Departure Delay (mins)'].apply(lambda x: x + 1440 if x < -720 else x)

        # Predict status
        df['Status'] = df['Departure Delay (mins)'].apply(lambda x: 'Delayed' if x > 15 else 'On Time')

        # Show results
        st.subheader("Processed Data")
        st.write(df[['Scheduled Departure Time', 'Actual Departure Time', 'Departure Delay (mins)', 'Status']].head())

        # Allow download
        st.download_button("Download Results", df.to_csv(index=False), "predicted_delays.csv", "text/csv")
