import streamlit as st
import pandas as pd
import datetime

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="V3.3 Alpha Sniper LIVE", layout="wide")

# V3.3 THEME STYLING
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_content_html=True)

st.title("🎯 V3.3 Alpha Sniper: Live Mechanical Audit")

# --- STEP 1: LIVE TRACK SELECTION ---
# In a full production app, this list is pulled automatically from the daily schedule.
tracks = ["Newmarket (Rowley)", "Ascot", "Goodwood", "Punchestown", "Limerick", "Chester"]
selected_track = st.selectbox("🏟️ Select Live Track for Audit", tracks)

# --- STEP 2: LIVE DATA FETCHING ENGINE ---
def get_live_data(track):
    # This simulates a LIVE API call to The Racing API or similar service
    # It pulls: Horse, Stall, OR, RPR, Weight, Gear, and Past Geometry
    if track == "Newmarket (Rowley)":
        return [
            {"Time": "15:35", "Horse": "Bow Echo", "Stall": 4, "OR": 115, "RPR": 128, "Wgt": 9.2, "Last_Wgt": 9.2, "Gear": "None", "Prev_Geo": "Straight", "Odds": 4.0},
            {"Time": "15:35", "Horse": "Oxagon", "Stall": 10, "OR": 109, "RPR": 120, "Wgt": 9.2, "Last_Wgt": 8.12, "Gear": "v1", "Prev_Geo": "Straight", "Odds": 11.0}
        ]
    elif track == "Punchestown":
        return [
            {"Time": "14:30", "Horse": "Beauvallon", "Stall": 0, "OR": 110, "RPR": 125, "Wgt": 11.4, "Last_Wgt": 11.0, "Gear": "None", "Prev_Geo": "Right", "Odds": 29.0}
        ]
    return []

live_race_data = get_live_data(selected_track)

# --- STEP 3: V3.3 MECHANICAL LOGIC ENGINE ---
if live_race_data:
    st.subheader(f"Analyzing {selected_track} - {datetime.date.today()}")
    
    for entry in live_race_data:
        # 1. Calculation Engine
        gap = entry['RPR'] - entry['OR']
        weight_diff = entry['Wgt'] - entry['Last_Wgt']
        is_sniper = entry['Odds'] >= 8.0 and gap >= 7
        is_alpha = gap >= 10 and entry['Odds'] >= 2.5
        
        # 2. Geometry & Track Bias Logic
        track_bias = "Favored" if entry['Stall'] > 0 and entry['Stall'] <= 6 else "Neutral"
        
        # 3. UI Display
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            
            with col1:
                st.metric(entry['Time'], entry['Horse'])
                
            with col2:
                st.write(f"**OR:** {entry['OR']} | **RPR:** {entry['RPR']} | **Gap:** +{gap}")
                st.write(f"**Gear:** {entry['Gear']} | **Weight Change:** +{weight_diff}st")
            
            with col3:
                if is_sniper:
                    st.error("🔫 SNIPER FIRE DETECTED")
                elif is_alpha:
                    st.success("🔥 ALPHA LOCK STATUS")
                else:
                    st.info("🔎 Analyzing Patterns...")
                
                if entry['Gear'] in ['v1', 't1']:
                    st.warning(f"⚙️ NEW GEAR ALPHA: {entry['Gear']}")
            
            with col4:
                st.metric("Odds", f"{entry['Odds']}")
                if track_bias == "Favored":
                    st.write("📍 **Stall Bias: HIGH**")
            
            st.divider()
else:
    st.write("No live data found for this track currently. Scanning other cards...")


