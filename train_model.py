import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load data
school = pd.read_csv("data/school_attendance.csv")
medicine = pd.read_csv("data/medicine_sales.csv")
toilet = pd.read_csv("data/toilet_usage.csv")
water = pd.read_csv("data/water_quality.csv")

# Merge data on date
df = school.merge(medicine, on="date") \
           .merge(toilet, on="date") \
           .merge(water, on="date")

# Feature engineering
df["absence_percent"] = (df["absent_students"] / df["total_students"]) * 100

# Risk labeling (ground truth)
conditions = [
    (df["absence_percent"] < 10) & (df["cold_cough_sales"] < 40),
    (df["absence_percent"] < 20),
    (df["absence_percent"] >= 20)
]

choices = [0, 1, 2]  # 0=Normal, 1=Alert, 2=Emergency
df["risk_label"] = np.select(conditions, choices)

features = [
    "absence_percent",
    "cold_cough_sales",
    "fever_sales",
    "usage_count",
    "ph",
    "turbidity"
]

X = df[features]
y = df["risk_label"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/risk_model.pkl")

print("✅ AI model trained and saved successfully")
