import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import json
import os

# Zodiac sign data
zodiac_signs = {
    "Aries":       {"emoji": "♈", "color": "#FFADAD", "range": ((3, 21), (4, 19)), "trait": "Bold and ambitious"},
    "Taurus":      {"emoji": "♉", "color": "#FFD6A5", "range": ((4, 20), (5, 20)), "trait": "Reliable and patient"},
    "Gemini":      {"emoji": "♊", "color": "#FDFFB6", "range": ((5, 21), (6, 20)), "trait": "Witty and curious"},
    "Cancer":      {"emoji": "♋", "color": "#CAFFBF", "range": ((6, 21), (7, 22)), "trait": "Intuitive and caring"},
    "Leo":         {"emoji": "♌", "color": "#9BF6FF", "range": ((7, 23), (8, 22)), "trait": "Confident and charismatic"},
    "Virgo":       {"emoji": "♍", "color": "#A0C4FF", "range": ((8, 23), (9, 22)), "trait": "Analytical and kind"},
    "Libra":       {"emoji": "♎", "color": "#BDB2FF", "range": ((9, 23), (10, 22)), "trait": "Balanced and fair"},
    "Scorpio":     {"emoji": "♏", "color": "#FFC6FF", "range": ((10, 23), (11, 21)), "trait": "Passionate and brave"},
    "Sagittarius": {"emoji": "♐", "color": "#FFFFFC", "range": ((11, 22), (12, 21)), "trait": "Adventurous and optimistic"},
    "Capricorn":   {"emoji": "♑", "color": "#D0F4DE", "range": ((12, 22), (1, 19)), "trait": "Disciplined and wise"},
    "Aquarius":    {"emoji": "♒", "color": "#FFCFD2", "range": ((1, 20), (2, 18)), "trait": "Independent and visionary"},
    "Pisces":      {"emoji": "♓", "color": "#F1C0E8", "range": ((2, 19), (3, 20)), "trait": "Empathetic and artistic"},
}

# Horoscope predictions
predictions = [
    "Today you will find unexpected joy in simple things 🌈",
    "Keep your eyes open — an opportunity is near 👀",
    "Trust your instincts — they’re right today 🔮",
    "Be bold — fortune favors the brave 🚀",
    "Take a deep breath — peace is within you 🌿",
    "Someone close to you has good news 🎉",
    "A creative spark will ignite your mind today 🎨",
]

# Determine zodiac sign from birthdate
def calculate_zodiac(month, day):
    for sign, data in zodiac_signs.items():
        start, end = data["range"]
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
        # Handle Capricorn wrap around
        if sign == "Capricorn" and ((month == 12 and day >= 22) or (month == 1 and day <= 19)):
            return "Capricorn"
    return None

# Get saved prediction or generate a new one (per sign, per date)
def get_daily_prediction(sign):
    filename = "daily_vision.json"
    today_str = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            saved = json.load(f)
    else:
        saved = {}

    # If today's prediction for the sign exists, use it
    if today_str in saved and sign in saved[today_str]:
        return saved[today_str][sign]["prediction"], saved[today_str][sign]["color"]

    # Generate new prediction
    prediction = random.choice(predictions)
    emoji = zodiac_signs[sign]["emoji"]
    trait = zodiac_signs[sign]["trait"]
    color = zodiac_signs[sign]["color"]

    text = f"{emoji} {sign} — {trait}\n\n✨ Today's Vision:\n{prediction}"

    # Save new prediction
    if today_str not in saved:
        saved[today_str] = {}
    saved[today_str][sign] = {
        "prediction": text,
        "color": color
    }

    with open(filename, "w") as f:
        json.dump(saved, f, indent=2)

    return text, color

# Main action on button click
def reveal_prediction():
    sign = zodiac_var.get()
    date_str = birth_entry.get().strip()

    if not sign and not date_str:
        messagebox.showerror("Input Error", "Please select a zodiac sign or enter a birthdate.")
        return

    if date_str:
        try:
            birthdate = datetime.strptime(date_str, "%Y-%m-%d")
            sign = calculate_zodiac(birthdate.month, birthdate.day)
            if not sign:
                raise ValueError
        except ValueError:
            messagebox.showerror("Date Error", "Please enter date as YYYY-MM-DD.")
            return

    result_text, bg_color = get_daily_prediction(sign)
    result_label.config(text=result_text, bg=bg_color)

# GUI setup
root = tk.Tk()
root.title("Horoscope Game - Reveal Today's Vision 🔮")
root.geometry("500x400")
root.resizable(False, False)

title_label = tk.Label(root, text="🌟 Horoscope Game 🌟", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

# Dropdown menu
tk.Label(frame, text="Select your zodiac sign:").grid(row=0, column=0, padx=5)
zodiac_var = tk.StringVar()
zodiac_menu = ttk.Combobox(frame, textvariable=zodiac_var, values=list(zodiac_signs.keys()), state="readonly")
zodiac_menu.grid(row=0, column=1, padx=5)

# Birthdate input
tk.Label(frame, text="Or enter birthdate (YYYY-MM-DD):").grid(row=1, column=0, padx=5)
birth_entry = tk.Entry(frame)
birth_entry.grid(row=1, column=1, padx=5)

# Button to reveal prediction
reveal_btn = tk.Button(root, text="🔍 Reveal Today’s Vision", font=("Helvetica", 14), command=reveal_prediction)
reveal_btn.pack(pady=15)

# Result display
result_label = tk.Label(root, text="", wraplength=400, font=("Helvetica", 13), relief="groove", bd=2, padx=10, pady=10)
result_label.pack(pady=10, fill="both", expand=True)

root.mainloop()
