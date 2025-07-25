import streamlit as st
import json
from datetime import datetime

# Set Streamlit page title and icon
st.set_page_config(page_title="Horoscope Game", page_icon="🔮")

st.title("🔮 Horoscope Game")

# --- Load Horoscope Data ---
with open("daily_vision.json", "r") as f:
    visions = json.load(f)

# --- Zodiac Date Ranges ---
zodiac_ranges = {
    "Aries":       ((3, 21),  (4, 19)),
    "Taurus":      ((4, 20),  (5, 20)),
    "Gemini":      ((5, 21),  (6, 20)),
    "Cancer":      ((6, 21),  (7, 22)),
    "Leo":         ((7, 23),  (8, 22)),
    "Virgo":       ((8, 23),  (9, 22)),
    "Libra":       ((9, 23),  (10, 22)),
    "Scorpio":     ((10, 23), (11, 21)),
    "Sagittarius": ((11, 22), (12, 21)),
    "Capricorn":   ((12, 22), (1, 19)),
    "Aquarius":    ((1, 20),  (2, 18)),
    "Pisces":      ((2, 19),  (3, 20)),
}

# --- Extract Only Zodiac Signs ---
zodiac_signs = [z for z in visions.keys() if z.lower() in [zod.lower() for zod in zodiac_ranges.keys()]]

# --- Select or Auto-detect Zodiac Sign ---
col1, col2 = st.columns(2)

with col1:
    selected_sign = st.selectbox("Select your zodiac sign", [""] + zodiac_signs)

with col2:
    birthdate_input = st.text_input("Or enter birthdate (YYYY-MM-DD)")

# --- Convert birthdate to zodiac if provided ---
def detect_zodiac(month: int, day: int) -> str:
    for sign, ((start_m, start_d), (end_m, end_d)) in zodiac_ranges.items():
        if ((month == start_m and day >= start_d) or
            (month == end_m and day <= end_d) or
            (start_m > end_m and (month == start_m or month == end_m))):  # handles Capricorn wrap
            return sign
    return "Unknown"

if birthdate_input:
    try:
        bdate = datetime.strptime(birthdate_input, "%Y-%m-%d")
        selected_sign = detect_zodiac(bdate.month, bdate.day)
        st.success(f"Detected zodiac sign: {selected_sign}")
    except ValueError:
        st.error("Invalid date format. Use YYYY-MM-DD.")

# --- Show Horoscope if Valid Sign ---
if st.button("🔍 Reveal Today’s Vision") and selected_sign:
    vision = visions.get(selected_sign)
    if vision:
        st.subheader(f"✨ Today's Vision for {selected_sign}")
        st.write(vision)
    else:
        st.warning("No vision found for this zodiac sign.")
