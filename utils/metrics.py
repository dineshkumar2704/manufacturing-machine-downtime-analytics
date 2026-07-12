import math
from datetime import datetime, timedelta


# ---------------------------------------------------------
# BASIC METRICS
# ---------------------------------------------------------
def calculate_basic_metrics(machine_df):
    total_downtime = machine_df["Downtime_Hours"].sum()
    planned_hours = machine_df["Planned_Work_Hours"].sum()
    actual_hours = machine_df["Actual_Work_Hours"].sum()

    utilization = actual_hours / planned_hours if planned_hours > 0 else 0
    downtime_pct = total_downtime / planned_hours if planned_hours > 0 else 0

    return total_downtime, utilization, downtime_pct


# ---------------------------------------------------------
# SMOOTH FAILURE PROBABILITY (NO 100% SPIKE)
# ---------------------------------------------------------
def calculate_failure_probability(total_downtime, max_expected=8):
    prob = 1 - math.exp(-total_downtime / max_expected)
    return round(prob, 2)


# ---------------------------------------------------------
# MACHINE HEALTH SCORE (BALANCED)
# ---------------------------------------------------------
def calculate_health_score(downtime_pct, failure_prob, utilization):
    health = (
        100
        - (downtime_pct * 30 * 100)
        - (failure_prob * 25)
        - ((1 - utilization) * 25 * 100)
    )

    return round(max(0, min(100, health)), 2)


# ---------------------------------------------------------
# HEALTH STATUS LABEL
# ---------------------------------------------------------
def get_health_status(health_score):
    if health_score >= 80:
        return "🟢 Healthy"
    elif health_score >= 50:
        return "🟡 Moderate"
    else:
        return "🔴 Critical"


# ---------------------------------------------------------
# PRIORITY LOGIC
# ---------------------------------------------------------
def calculate_priority(health_score, failure_prob):
    if health_score < 45 and failure_prob >= 0.7:
        return "HIGH"
    elif health_score < 70 or failure_prob >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"


# ---------------------------------------------------------
# EXPLANATION (WHY TRIGGERED)
# ---------------------------------------------------------
def generate_reasons(total_downtime, failure_prob, utilization, health_score):
    reasons = []

    if total_downtime > 3:
        reasons.append("Downtime exceeded normal monthly limit")

    if failure_prob >= 0.4:
        reasons.append("Failure probability above safe threshold")

    if utilization < 0.6:
        reasons.append("Low machine utilization detected")

    if health_score < 50:
        reasons.append("Machine health is in critical condition")

    if not reasons:
        reasons.append("Machine operating within acceptable parameters")

    return reasons


# ---------------------------------------------------------
# MAINTENANCE DATE
# ---------------------------------------------------------
def suggest_maintenance_date(priority):
    today = datetime.today()

    if priority == "HIGH":
        return (today + timedelta(days=1)).strftime("%d %b %Y")
    elif priority == "MEDIUM":
        return (today + timedelta(days=4)).strftime("%d %b %Y")
    else:
        return (today + timedelta(days=10)).strftime("%d %b %Y")
