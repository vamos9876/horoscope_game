import streamlit as st
import json
import datetime
from pathlib import Path

st.set_page_config(page_title="Horoscope Game", page_icon="🔮")

st.title("🔮 Horoscope Game")

# Load JSON file
with open("daily_vision.json") as f:
    visions = json.load(f)

# Zodiac signs
zodiacs = list(visions.keys())

# UI
col1, col2 = st.columns(2)
selected_sign = col1.selectbox("Select your zodiac sign", [""] + zodiacs)
birthdate = col2.text_input("Or enter birthdate (YYYY-MM-DD)")

# Determine today's index
today = datetime.datetime.now().day % 3  # Cycles 0–2

# Button
if st.button("🔍 Reveal Today’s Vision"):
    if birthdate:
        st.markdown("☝️ Birthdate input not yet used in logic.")
    elif selected_sign:
        vision = visions[selected_sign][today]
        st.markdown(f"### ✨✨ {vision} ✨✨")
        st.markdown("<p style='text-align: center; font-size: 16px; color: grey;'>Don't ignore it.</p>", unsafe_allow_html=True)
    else:
        st.warning("Please select your zodiac sign or enter birthdate.")
