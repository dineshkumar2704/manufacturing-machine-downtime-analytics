from datetime import datetime, timedelta

def generate_advanced_recommendation(
    machine,
    downtime_hours,
    failure_prob,
    total_cost
):
    reasons = []

    # -----------------------------
    # PRIORITY LOGIC
    # -----------------------------
    if failure_prob >= 0.7 or total_cost > 50000:
        priority = "HIGH"
    elif failure_prob >= 0.4:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    # -----------------------------
    # REASONS (EXPLAINABILITY)
    # -----------------------------
    if downtime_hours > 2:
        reasons.append("Downtime exceeded SLA limit (2 hours)")

    if failure_prob >= 0.7:
        reasons.append("High ML-predicted failure probability")

    if total_cost > 50000:
        reasons.append("High financial loss due to downtime")

    if not reasons:
        reasons.append("Machine operating within acceptable limits")

    # -----------------------------
    # CONFIDENCE SCORE (0–100%)
    # -----------------------------
    confidence = round(
        (failure_prob * 0.4 + min(downtime_hours / 5, 1) * 0.3 + min(total_cost / 100000, 1) * 0.3) * 100,
        2
    )

    # -----------------------------
    # MAINTENANCE DATE SUGGESTION
    # -----------------------------
    today = datetime.today()

    if priority == "HIGH":
        maintenance_date = today + timedelta(days=1)
    elif priority == "MEDIUM":
        maintenance_date = today + timedelta(days=4)
    else:
        maintenance_date = today + timedelta(days=10)

    return {
        "machine": machine,
        "priority": priority,
        "confidence": confidence,
        "reasons": reasons,
        "maintenance_date": maintenance_date.strftime("%d %b %Y"),
    }
