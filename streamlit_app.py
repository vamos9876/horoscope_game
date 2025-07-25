import streamlit as st
import pandas as pd
import random
import time
import json
from datetime import datetime

# 🎨 Page setup
st.set_page_config(page_title="Horoscope Game", page_icon="🔮")

st.markdown("<h1 style='text-align: center;'>🔮 Horoscope Game 🔮</h1>", unsafe_allow_html=True)

# 🎯 Load visions (daily messages)
with open("daily_vision.json", "r") as f:
    visions = json.load(f)

zodiac_signs = list(visions.keys())

col1, col2 = st.columns(2)

selected_sign = col1.selectbox("Select your zodiac sign", options=zodiac_signs)
birthdate = col2.text_input("Or enter birthdate (YYYY-MM-DD)")

st.markdown("<br>", unsafe_allow_html=True)

# 🚀 Button to reveal vision
if st.button("🔍 Reveal Today’s Vision"):
    with st.spinner("✨ Reading the stars..."):
        time.sleep(3)  # Delay effect like "magic"
    
    # 🌟 Select vision
    if selected_sign:
        today = datetime.now().date()
        random.seed(f"{selected_sign}-{today}")  # ensure one vision per day per sign
        vision = random.choice(visions[selected_sign])
        st.markdown(f"<h2 style='text-align: center;'>✨✨ {vision} ✨✨</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Don't ignore it.</p>", unsafe_allow_html=True)
