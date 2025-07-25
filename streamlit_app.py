import streamlit as st
import json
from datetime import date
from pathlib import Path
import hashlib

# --- Load horoscope data safely ---
visions_path = Path(__file__).parent / "daily_vision.json"

try:
    with open(visions_path, "r") as f:
        visions_data = json.load(f)
except Exception as e:
    st.error("❌ Failed to load horoscope data. Please check daily_vision.json.")
    st.stop()

# --- App UI ---
st.set_page_config(page_title="Horoscope Game", page_icon="🔮")
st.title("🔮 Horoscope Game 🔮")

col1, col2 = st.columns(2)
with col1:
    sign = st.selectbox("Select your zodiac sign", options=list(visions_data.keys()))
with col2:
    birthdate = st.text_input("Or enter birthdate (YYYY-MM-DD)")

# Optional: Derive sign from date (not implemented here)
# You could use a library like `zodiac-sign` or custom mapping.

# --- Determine "stable" vision based on today's date ---
def get_daily_index(options, sign):
    """Returns a stable index based on today's date and sign."""
    today_str = date.today().isoformat() + sign
    hashed = hashlib.sha256(today_str.encode()).hexdigest()
    return int(hashed, 16) % len(options)

# --- Button logic ---
if st.button("🔍 Reveal Today’s Vision"):
    if sign and sign in visions_data:
        messages = visions_data[sign]
        i = get_daily_index(messages, sign)
        vision = messages[i]
        st.markdown(f"### ✨✨ {vision} ✨✨")
st.markdown("<p style='text-align: center; font-size: 16px; color: grey;'>Don't ignore it.</p>", unsafe_allow_html=True)
    else:
        st.warning("Please select a valid zodiac sign.")
