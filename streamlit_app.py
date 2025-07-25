import streamlit as st
import json
from datetime import datetime

# Load vision data
with open("daily_vision.json", "r") as f:
    visions = json.load(f)

zodiac_signs = list(visions.keys())

st.set_page_config(page_title="Horoscope Game", page_icon="🔮")
st.title("🔮 Horoscope Game")

# UI
zodiac = st.selectbox("Select your zodiac sign", zodiac_signs)
birthdate = st.text_input("Or enter birthdate (YYYY-MM-DD)")

if st.button("🔍 Reveal Today’s Vision"):
    if zodiac:
        vision = visions.get(zodiac, "No vision found.")
        st.success(f"✨ {vision}")
