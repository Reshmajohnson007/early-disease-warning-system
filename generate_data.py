import pandas as pd
import numpy as np

np.random.seed(42)

DAYS = 20000
dates = pd.date_range(start="2000-01-01", periods=DAYS)

# ---------- SCHOOL ATTENDANCE ----------
total_students = 200
absent_base = np.random.normal(8, 2, DAYS)

# outbreak spikes
spike_days = np.random.choice(DAYS, size=120, replace=False)
absent_base[spike_days] += np.random.randint(20, 60, size=120)

absent_students = np.clip(absent_base.astype(int), 0, total_students)

school_df = pd.DataFrame({
    "date": dates,
    "total_students": total_students,
    "absent_students": absent_students
})

# ---------- MEDICINE SALES ----------
cold_sales = np.random.normal(20, 6, DAYS)
fever_sales = np.random.normal(10, 4, DAYS)

cold_sales[spike_days] += np.random.randint(30, 80, size=120)
fever_sales[spike_days] += np.random.randint(20, 60, size=120)

medicine_df = pd.DataFrame({
    "date": dates,
    "cold_cough_sales": np.clip(cold_sales.astype(int), 0, None),
    "fever_sales": np.clip(fever_sales.astype(int), 0, None)
})

# ---------- TOILET USAGE ----------
usage = np.random.normal(300, 40, DAYS)
usage[spike_days] += np.random.randint(150, 400, size=120)

toilet_df = pd.DataFrame({
    "date": dates,
    "usage_count": np.clip(usage.astype(int), 0, None)
})

# ---------- WATER QUALITY ----------
ph = np.random.normal(7.2, 0.3, DAYS)
turbidity = np.random.normal(3, 1, DAYS)

ph[spike_days] -= np.random.uniform(0.8, 1.5, size=120)
turbidity[spike_days] += np.random.uniform(3, 6, size=120)

water_df = pd.DataFrame({
    "date": dates,
    "ph": np.round(ph, 2),
    "turbidity": np.round(turbidity, 2)
})

# ---------- SAVE FILES ----------
school_df.to_csv("data/school_attendance.csv", index=False)
medicine_df.to_csv("data/medicine_sales.csv", index=False)
toilet_df.to_csv("data/toilet_usage.csv", index=False)
water_df.to_csv("data/water_quality.csv", index=False)

print("✅ 20,000-sample datasets generated successfully")
