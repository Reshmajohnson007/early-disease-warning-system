import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3
import time

from government_report import generate_report
from sms_service import send_sms

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Early Disease Warning", layout="wide")

# ---------- TITLE ----------
st.title("🦠 AI-Based Early Disease Warning System")

# ---------- REFRESH BUTTON ----------
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.experimental_rerun()

# ---------- LOAD DATA ----------
@st.cache_data(ttl=10)
def load_data():
    school = pd.read_csv("data/school_attendance.csv")
    medicine = pd.read_csv("data/medicine_sales.csv")
    toilet = pd.read_csv("data/toilet_usage.csv")
    water = pd.read_csv("data/water_quality.csv")
    return school, medicine, toilet, water

school, medicine, toilet, water = load_data()

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

# ---------- DISPLAY STATUS ----------
st.markdown(f"### **Current Status:** :{color}[{status}]")
st.metric("Risk Score", f"{risk_score} / 100")

# ---------- TREND ----------
st.subheader("📈 Risk Trend (Last 7 Days)")
trend = school.tail(7)["absent_students"]
st.line_chart(trend)

# ---------- REASONS ----------
st.subheader("⚠️ Reasons")
st.write(f"- School Absence: {absence_rate:.2f}%")
st.write("- Medicine Sales Spike")
st.write("- Toilet Usage Increased")
st.write("- Water Quality Decline")

# ---------- GOVERNMENT AUTO-REPORT ----------
if risk_score >= 40:
    reasons = """
- School absenteeism increased
- Medicine sales spiked
- Water quality abnormal
"""
    report_file = generate_report(risk_score, status, reasons)
    st.success(f"📄 Government report generated: {report_file}")

# ---------- SMS ALERT ----------
if risk_score >= 60:
    send_sms(
        "+91XXXXXXXXXX",
        "🚨 Emergency Alert: Disease risk is HIGH in your village. Please take precautions."
    )
    st.error("📱 SMS alert sent to villagers")

# ---------- VOICE ALERT ----------
if status == "EMERGENCY":
    engine = pyttsx3.init()
    engine.say("Emergency alert. Disease risk is very high in the village.")
    engine.runAndWait()

# ---------- TIMESTAMP ----------
st.caption(f"Last updated at: {time.strftime('%H:%M:%S')}")
