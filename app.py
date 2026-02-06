import streamlit as st
import pandas as pd
import random
import time
import pyttsx3
from datetime import datetime

from government_report import generate_report
from sms_service import send_sms

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Early Disease Warning", layout="wide")

# ---------- SESSION STATE ----------
if "last_status" not in st.session_state:
    st.session_state.last_status = None

# ---------- AUTO DATA GENERATION ----------
def auto_generate_data():
    # SCHOOL
    school = pd.read_csv("data/school_attendance.csv")
    total = school.iloc[-1]["total_students"]
    absent = max(0, school.iloc[-1]["absent_students"] + random.randint(-2, 10))
    school.loc[len(school)] = [datetime.now().strftime("%Y-%m-%d"), total, absent]
    school.to_csv("data/school_attendance.csv", index=False)

    # MEDICINE
    medicine = pd.read_csv("data/medicine_sales.csv")
    cold = max(0, medicine.iloc[-1]["cold_cough_sales"] + random.randint(0, 5))
    fever = max(0, medicine.iloc[-1]["fever_sales"] + random.randint(0, 5))
    medicine.loc[len(medicine)] = [datetime.now().strftime("%Y-%m-%d"), cold, fever]
    medicine.to_csv("data/medicine_sales.csv", index=False)

    # TOILET
    toilet = pd.read_csv("data/toilet_usage.csv")
    usage = max(0, toilet.iloc[-1]["usage_count"] + random.randint(0, 15))
    toilet.loc[len(toilet)] = [datetime.now().strftime("%Y-%m-%d"), usage]
    toilet.to_csv("data/toilet_usage.csv", index=False)

    # WATER
    water = pd.read_csv("data/water_quality.csv")
    ph = round(random.uniform(6.0, 8.5), 2)
    turbidity = random.randint(1, 10)
    water.loc[len(water)] = [datetime.now().strftime("%Y-%m-%d"), ph, turbidity]
    water.to_csv("data/water_quality.csv", index=False)

# ---------- TITLE ----------
st.title("🦠 AI-Based Early Disease Warning System")

# ---------- AUTO UPDATE BUTTON ----------
if st.button("▶ Generate New Data & Update Dashboard"):
    auto_generate_data()
    st.cache_data.clear()
    st.rerun()

# ---------- LOAD DATA ----------
@st.cache_data(ttl=0)
def load_data():
    return (
        pd.read_csv("data/school_attendance.csv"),
        pd.read_csv("data/medicine_sales.csv"),
        pd.read_csv("data/toilet_usage.csv"),
        pd.read_csv("data/water_quality.csv"),
    )

school, medicine, toilet, water = load_data()

# ---------- METRICS ----------
absence_rate = (school.iloc[-1]["absent_students"] / school.iloc[-1]["total_students"]) * 100
medicine_total = medicine.iloc[-1][["cold_cough_sales", "fever_sales"]].sum()
toilet_usage = toilet.iloc[-1]["usage_count"]
ph = water.iloc[-1]["ph"]
turbidity = water.iloc[-1]["turbidity"]

# ---------- BALANCED RISK SCORE ----------
school_risk = min((absence_rate / 30) * 25, 25)
medicine_risk = min((medicine_total / 50) * 25, 25)
toilet_risk = min((toilet_usage / 200) * 25, 25)
water_risk = min((abs(7 - ph) * 10 + turbidity) / 20 * 25, 25)

risk_score = int(school_risk + medicine_risk + toilet_risk + water_risk)

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

# ---------- DISPLAY ----------
st.markdown(f"### Status: :{color}[{status}]")
st.metric("Risk Score", f"{risk_score} / 100")
st.progress(risk_score / 100)

# ---------- TREND ----------
st.subheader("📈 School Absence Trend")
st.line_chart(school.tail(7)["absent_students"])

# ---------- AUTO REPORT ----------
if risk_score >= 40:
    report = generate_report(
        risk_score,
        status,
        "Multiple health indicators exceeded safe thresholds"
    )
    st.success(f"📄 Government report generated: {report}")

# ---------- ALERTS (ONCE PER CHANGE) ----------
if status != st.session_state.last_status:
    if status == "EMERGENCY":
        engine = pyttsx3.init()
        engine.say("Emergency alert. Disease risk is very high in the village.")
        engine.runAndWait()

        send_sms(
            "+91XXXXXXXXXX",
            "Emergency Alert: Disease risk is high. Take precautions."
        )

    st.session_state.last_status = status

# ---------- TIME ----------
st.caption(f"Last updated at {time.strftime('%H:%M:%S')}")
