import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Early Disease Warning", layout="wide")

# ---------- LOAD DATA ----------
school = pd.read_csv("data/school_attendance.csv")
medicine = pd.read_csv("data/medicine_sales.csv")
toilet = pd.read_csv("data/toilet_usage.csv")
water = pd.read_csv("data/water_quality.csv")

# ---------- CALCULATE RISK ----------
absence_rate = (school.iloc[-1]["absent_students"] / school.iloc[-1]["total_students"]) * 100
medicine_rate = medicine.iloc[-1][["cold_cough_sales", "fever_sales"]].sum()
toilet_rate = toilet.iloc[-1]["usage_count"] / 10
water_risk = abs(7 - water.iloc[-1]["ph"]) * 10 + water.iloc[-1]["turbidity"]

risk_score = int(absence_rate + medicine_rate + toilet_rate + water_risk)
risk_score = min(risk_score, 100)

# ---------- STATUS ----------
if risk_score <= 30:
    status = "NORMAL"
    color = "green"
elif risk_score <= 60:
    status = "ALERT"
    color = "orange"
else:
    status = "EMERGENCY"
    color = "red"

# ---------- HEADER ----------
st.title("🦠 AI-Based Early Disease Warning System")
st.markdown(f"### **Current Status:** :{color}[{status}]")
st.metric("Risk Score", f"{risk_score} / 100")

# ---------- TREND ----------
st.subheader("📈 Risk Trend (Last 7 Days)")
trend = school.tail(7)["absent_students"].values
st.line_chart(trend)

# ---------- REASONS ----------
st.subheader("⚠️ Reasons")
st.write(f"- School Absence: {absence_rate:.2f}%")
st.write(f"- Medicine Sales Spike")
st.write(f"- Toilet Usage Increased")
st.write(f"- Water Quality Decline")

# ---------- VOICE ALERT ----------
if status == "EMERGENCY":
    engine = pyttsx3.init()
    engine.say("Emergency alert. Disease risk is very high in the village.")
    engine.runAndWait()
