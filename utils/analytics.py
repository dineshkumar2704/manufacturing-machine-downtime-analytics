import numpy as np

def calculate_oee(df):
    if df.empty:
        return 0

    availability = (df["Actual_Work_Hours"].sum() / df["Planned_Work_Hours"].sum()) * 100
    performance = ((df["Planned_Work_Hours"].sum() - df["Downtime_Hours"].sum()) / df["Planned_Work_Hours"].sum()) * 100
    quality = 100  # Assume 100% because dataset does not include defects

    oee = (availability * performance * quality) / 10000 * 100
    return round(oee, 2)

def calculate_health_score(df):
    if df.empty:
        return 0

    utilization = (df["Actual_Work_Hours"].sum() / df["Planned_Work_Hours"].sum()) * 100
    downtime_pct = (df["Downtime_Hours"].sum() / df["Planned_Work_Hours"].sum()) * 100
    failure_frequency = np.where(df["Downtime_Hours"] > 2, 1, 0).sum()

    score = 100 - (downtime_pct * 0.4) - (failure_frequency * 2) - ((100 - utilization) * 0.3)
    return max(0, min(100, round(score, 2)))
